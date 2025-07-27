import os
import tempfile
import uuid
from flask import Flask, render_template, request, send_file, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "development-secret-key")

# Create upload and output directories if they don't exist
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file:
        # Generate a unique filename
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)
        
        # Get compression parameters
        block_size = request.form.get('block_size', '4x4')
        color_profile = request.form.get('color_profile', 'srgb')
        quality = int(request.form.get('quality', '75'))
        
        # Save parameters in session
        session['input_path'] = input_path
        session['original_filename'] = file.filename
        session['block_size'] = block_size
        session['color_profile'] = color_profile
        session['quality'] = quality
        
        return redirect(url_for('preview'))

@app.route('/preview')
def preview():
    if 'input_path' not in session:
        flash('No image uploaded')
        return redirect(url_for('index'))
    
    input_path = session.get('input_path')
    original_filename = session.get('original_filename')
    block_size = session.get('block_size')
    color_profile = session.get('color_profile')
    quality = session.get('quality')
    
    # Run a test compression to get metrics
    import astc_encoder.metrics as metrics
    try:
        metrics_result = metrics.compute_metrics(
            input_path=input_path,
            block_size=block_size,
            color_profile=color_profile,
            quality=quality
        )
    except Exception as e:
        flash(f'Error computing metrics: {str(e)}')
        metrics_result = {
            'psnr': 'Error',
            'ssim': 'Error',
            'compression_ratio': 'Error',
            'original_size_formatted': 'Unknown',
            'compressed_size_formatted': 'Unknown'
        }
    
    return render_template(
        'preview.html',
        filename=original_filename,
        input_path=os.path.basename(input_path),
        block_size=block_size,
        color_profile=color_profile,
        quality=quality,
        metrics=metrics_result
    )

@app.route('/compress')
def compress():
    if 'input_path' not in session:
        flash('No image uploaded')
        return redirect(url_for('index'))
    
    input_path = session.get('input_path')
    original_filename = session.get('original_filename')
    block_size = session.get('block_size')
    color_profile = session.get('color_profile')
    quality = session.get('quality')
    
    # Create output filenames
    base_name = os.path.splitext(original_filename)[0]
    astc_filename = f"{base_name}_{block_size}.astc"
    output_astc_path = os.path.join(OUTPUT_FOLDER, astc_filename)
    
    # Compress the image
    import astc_encoder.encoder as encoder
    try:
        encoder.compress_image(
            input_path=input_path,
            output_path=output_astc_path,
            block_size=block_size,
            color_profile=color_profile,
            quality=quality
        )
        
        # Generate a decompressed image for comparison
        decompressed_filename = f"{base_name}_{block_size}_decompressed.png"
        output_decompressed_path = os.path.join(OUTPUT_FOLDER, decompressed_filename)
        
        import astc_encoder.decoder as decoder
        decoder.decompress_image(
            input_path=output_astc_path,
            output_path=output_decompressed_path,
            color_profile=color_profile
        )
        
        # Save output paths in session
        session['output_astc_path'] = output_astc_path
        session['output_decompressed_path'] = output_decompressed_path
        session['astc_filename'] = astc_filename
        session['decompressed_filename'] = decompressed_filename
        
        flash('Compression completed successfully')
    except Exception as e:
        flash(f'Error during compression: {str(e)}')
    
    return redirect(url_for('results'))

@app.route('/results')
def results():
    if 'input_path' not in session or 'output_astc_path' not in session:
        flash('No compression results available')
        return redirect(url_for('index'))
    
    input_path = session.get('input_path')
    output_astc_path = session.get('output_astc_path')
    output_decompressed_path = session.get('output_decompressed_path')
    original_filename = session.get('original_filename')
    astc_filename = session.get('astc_filename')
    decompressed_filename = session.get('decompressed_filename')
    block_size = session.get('block_size')
    color_profile = session.get('color_profile')
    quality = session.get('quality')
    
    # Get file sizes
    original_size = os.path.getsize(input_path)
    compressed_size = os.path.getsize(output_astc_path)
    
    import astc_encoder.utils as utils
    original_size_formatted = utils.format_bytes(original_size)
    compressed_size_formatted = utils.format_bytes(compressed_size)
    compression_ratio = original_size / compressed_size if compressed_size > 0 else 0
    
    return render_template(
        'results.html',
        original_filename=original_filename,
        astc_filename=astc_filename,
        decompressed_filename=decompressed_filename,
        input_path=os.path.basename(input_path),
        block_size=block_size,
        color_profile=color_profile,
        quality=quality,
        original_size=original_size_formatted,
        compressed_size=compressed_size_formatted,
        compression_ratio=compression_ratio
    )

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

@app.route('/outputs/<filename>')
def output_file(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename))

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
