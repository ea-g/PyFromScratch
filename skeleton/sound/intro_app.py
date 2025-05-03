import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import io
import base64
from nicegui import ui, app
import tempfile
import os

# For serving audio files
app.add_static_files('/audio', 'audio_files')

def setup_visualization_tab():
    ui.label('Upload and Visualize Sound Files').classes('text-h5')
    
    # Create placeholder for the visualization
    plot_container = ui.card().classes('w-full')
    
    # Global variables to store audio data
    audio_data = {'sr': None, 'data': None, 'filename': None}
    
    def handle_upload(e):
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
            f.write(e.content.read())
            temp_filename = f.name
        
        # Read the audio file
        try:
            sr, data = wavfile.read(temp_filename)
            audio_data['sr'] = sr
            audio_data['data'] = data
            audio_data['filename'] = e.name
            
            # Create visualization
            update_visualization()
            
            # Copy file to static folder for playback
            os.makedirs('audio_files', exist_ok=True)
            playback_path = os.path.join('audio_files', e.name)
            with open(playback_path, 'wb') as f:
                with open(temp_filename, 'rb') as src:
                    f.write(src.read())
            
            # Update audio player
            audio_player.set_source(f'/audio/{e.name}')
            ui.notify(f'Successfully loaded {e.name}')
        except Exception as ex:
            ui.notify(f'Error loading audio: {str(ex)}', color='negative')
        finally:
            os.unlink(temp_filename)
    
    def update_visualization():
        if audio_data['data'] is None:
            return
        
        with plot_container:
            plot_container.clear()
            
            with ui.matplotlib(figsize=(8, 4)).figure as fig:
                ax = fig.add_subplot(111)
                
                # Get data for plotting
                data = audio_data['data']
                sr = audio_data['sr']
                
                # If stereo, only plot first channel
                if len(data.shape) > 1:
                    data = data[:, 0]
                
                # Calculate time axis
                time = np.arange(0, len(data)) / sr
                
                # Plot waveform
                ax.plot(time, data, linewidth=0.5)
                
                # Add labels and title
                ax.set_xlabel('Time (seconds)')
                ax.set_ylabel('Amplitude')
                ax.set_title(f'Waveform: {audio_data["filename"]}')
                
                # Add grid
                ax.grid(True, alpha=0.3)
                
                fig.tight_layout()
    
    # File upload component
    ui.upload(on_upload=handle_upload, label='Upload WAV file', auto_upload=True).props('accept=".wav"')
    
    # Audio playback
    with ui.row().classes('w-full items-center'):
        ui.label('Playback:')
        audio_player = ui.audio('').classes('w-full')

def setup_generator_tab():
    ui.label('Generate Custom Sound Waves').classes('text-h5')
    
    # Create parameters for sound generation
    with ui.card().classes('w-full'):
        with ui.row():
            with ui.column():
                frequency_slider = ui.slider(min=20, max=20000, value=440)
                ui.label().bind_text_from(frequency_slider, 'value', lambda v: f'Frequency: {v:.1f} Hz')
            
            with ui.column():
                amplitude_slider = ui.slider(min=0, max=1, value=0.5, step=0.01)
                ui.label().bind_text_from(amplitude_slider, 'value', lambda v: f'Amplitude: {v:.2f}')
        
        with ui.row():
            with ui.column():
                duration_slider = ui.slider(min=0.1, max=5, value=1, step=0.1)
                ui.label().bind_text_from(duration_slider, 'value', lambda v: f'Duration: {v:.1f} seconds')
            
            with ui.column():
                waveform_type = ui.select(['Sine', 'Square', 'Sawtooth', 'Triangle'], value='Sine', label='Waveform Type')
    
    # Create placeholder for visualization
    gen_plot_container = ui.card().classes('w-full')
    
    def generate_sound():
        # Get parameters
        frequency = frequency_slider.value
        amplitude = amplitude_slider.value
        duration = duration_slider.value
        wave_type = waveform_type.value
        
        # Set up sampling
        sample_rate = 44100  # Standard audio sample rate
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        
        # Generate waveform
        if wave_type == 'Sine':
            waveform = amplitude * np.sin(2 * np.pi * frequency * t)
        elif wave_type == 'Square':
            waveform = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
        elif wave_type == 'Sawtooth':
            waveform = amplitude * 2 * (t * frequency - np.floor(t * frequency + 0.5))
        elif wave_type == 'Triangle':
            waveform = amplitude * 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
        
        # Scale to 16-bit range and convert to integer
        waveform_int = np.int16(waveform * 32767)
        
        # Save to file
        filename = f"{wave_type.lower()}_{frequency}hz_{duration}s.wav"
        temp_path = os.path.join(tempfile.gettempdir(), filename)
        wavfile.write(temp_path, sample_rate, waveform_int)
        
        # Copy to static folder for playback
        os.makedirs('audio_files', exist_ok=True)
        playback_path = os.path.join('audio_files', filename)
        with open(playback_path, 'wb') as f:
            with open(temp_path, 'rb') as src:
                f.write(src.read())
        
        # Update audio player
        gen_audio_player.set_source(f'/audio/{filename}')
        
        # Update visualization
        update_gen_visualization(t, waveform, frequency, wave_type)
        
        ui.notify(f'Generated {wave_type} wave at {frequency} Hz')
    
    def update_gen_visualization(t, waveform, frequency, wave_type):
        with gen_plot_container:
            gen_plot_container.clear()
            
            with ui.matplotlib(figsize=(8, 6)).figure as fig:
                
                # Plot waveform
                ax1 = fig.add_subplot(211)
                ax1.plot(t[:int(44100/frequency*5)], waveform[:int(44100/frequency*5)], linewidth=1)
                ax1.set_title(f'{wave_type} Wave at {frequency} Hz')
                ax1.set_xlabel('Time (s)')
                ax1.set_ylabel('Amplitude')
                ax1.grid(True, alpha=0.3)
                
                # Plot frequency spectrum
                ax2 = fig.add_subplot(212)
                n = len(waveform)
                yf = np.fft.rfft(waveform)
                xf = np.fft.rfftfreq(n, 1/44100)
                ax2.semilogy(xf, np.abs(yf))
                ax2.set_title('Frequency Spectrum')
                ax2.set_xlabel('Frequency (Hz)')
                ax2.set_ylabel('Magnitude')
                ax2.set_xlim(0, min(20000, frequency*10))
                ax2.grid(True, alpha=0.3)
                
                fig.tight_layout()
    
    # Generate button
    ui.button('Generate Sound', on_click=generate_sound).classes('mt-4')
    
    # Audio playback
    with ui.row().classes('w-full items-center mt-4'):
        ui.label('Playback:')
        gen_audio_player = ui.audio('').classes('w-full')
    
    # Initial visualization with default values
    t = np.linspace(0, 1, 44100, endpoint=False)
    waveform = 0.5 * np.sin(2 * np.pi * 440 * t)
    update_gen_visualization(t, waveform, 440, 'Sine')

def setup_learning_tab():
    ui.label('Sound Physics and Perception').classes('text-h5')
    
    with ui.tabs().classes('w-full') as learn_tabs:
        physics_tab = ui.tab('Physics of Sound')
        hearing_tab = ui.tab('How We Hear')
        connections_tab = ui.tab('Making Connections')
    
    with ui.tab_panels(learn_tabs, value=physics_tab).classes('w-full'):
        with ui.tab_panel(physics_tab):
            ui.markdown('''
            ## Physics of Sound
            
            Sound is a mechanical wave that requires a medium to propagate. Key properties include:
            
            ### Frequency (Hz)
            - Determines the pitch of a sound
            - Human hearing range: 20 Hz to 20,000 Hz
            - Lower frequencies = lower pitches
            - Higher frequencies = higher pitches
            
            ### Amplitude
            - Determines the loudness/volume of a sound
            - Measured in decibels (dB)
            - Represents the magnitude of pressure variation
            
            ### Wavelength
            - The distance between consecutive corresponding points on a wave
            - Related to frequency by: Wavelength = Speed of Sound / Frequency
            
            ### Period
            - Time taken for one complete cycle of the wave
            - Related to frequency by: Period = 1 / Frequency
            
            ### Speed of Sound
            - In air at room temperature: ~343 meters/second
            - Varies with medium and temperature
            - Faster in solids and liquids than in gases
            ''')
            
            # Add an interactive visualization
            with ui.card().classes('w-full'):
                ui.label('Interactive Sound Wave').classes('text-h6')
                
                with ui.row():
                    with ui.column():
                        demo_freq_slider = ui.slider(min=1, max=10, value=1, step=0.1)
                        ui.label().bind_text_from(demo_freq_slider, 'value', lambda v: f'Frequency: {v:.1f} Hz')
                    with ui.column():
                        demo_amp_slider = ui.slider(min=0.1, max=2, value=1, step=0.1)
                        ui.label().bind_text_from(demo_amp_slider, 'value', lambda v: f'Amplitude: {v:.2f}')
                    
                demo_plot = ui.card().classes('w-full')
                
                def update_demo_plot():
                    with demo_plot:
                        demo_plot.clear()
                        
                        with ui.matplotlib(figsize=(8, 3)).figure as fig:
                            
                            ax = fig.add_subplot(111)
                            
                            # Generate wave
                            x = np.linspace(0, 1, 1000)
                            freq = demo_freq_slider.value
                            amp = demo_amp_slider.value
                            y = amp * np.sin(2 * np.pi * freq * x)
                            
                            # Plot
                            ax.plot(x, y)
                            ax.set_ylim(-2, 2)
                            ax.set_title(f'Sine Wave: Frequency = {freq}Hz, Amplitude = {amp}')
                            ax.set_xlabel('Time (s)')
                            ax.set_ylabel('Amplitude')
                            ax.grid(True, alpha=0.3)
                            
                            # Add wavelength annotation
                            wavelength = 1/freq
                            ax.annotate('', xy=(0.1, 0), xytext=(0.1 + wavelength, 0), 
                                        arrowprops=dict(arrowstyle='<->', color='red'))
                            ax.text(0.1 + wavelength/2, 0.1, 'Wavelength', ha='center', color='red')
                            
                            fig.tight_layout()
                
                demo_freq_slider.on('update:model-value', update_demo_plot)
                demo_amp_slider.on('update:model-value', update_demo_plot)
                
                # Initial plot
                update_demo_plot()
        
        with ui.tab_panel(hearing_tab):
            ui.markdown('''
            ## How We Hear
            
            Sound perception is a complex process involving mechanical, hydraulic, and neural components.
            
            ### The Journey of Sound
            
            1. **Collection**: The outer ear (pinna) collects and funnels sound waves into the ear canal
            2. **Conversion to Vibration**: Sound waves cause the eardrum (tympanic membrane) to vibrate
            3. **Amplification**: The middle ear bones (ossicles) amplify these vibrations
            4. **Fluid Waves**: Vibrations create waves in the fluid-filled cochlea
            5. **Hair Cell Response**: Specialized hair cells in the cochlea bend in response to these waves
            6. **Neural Signals**: Hair cells convert mechanical motion into electrical signals
            7. **Brain Processing**: Signals travel through the auditory nerve to the brain for processing
            
            ### The Auditory Pathway
            
            The neural processing of sound involves several key stations:
            
            - **Cochlear Nuclei**: First processing in the brainstem
            - **Superior Olivary Complex**: Important for sound localization
            - **Inferior Colliculus**: Further processing in the midbrain
            - **Medial Geniculate Body**: Processing in the thalamus
            - **Auditory Cortex**: Final processing, conscious perception of sound
            
            ### Frequency Perception
            
            The cochlea contains a remarkable feature called the basilar membrane, which vibrates at different positions depending on the frequency of the sound:
            
            - **Base of Cochlea**: Responds to high frequencies
            - **Apex of Cochlea**: Responds to low frequencies
            
            This "tonotopic organization" is maintained throughout the auditory pathway, creating a frequency map in the brain.
            ''')
            
            # Add an interactive cochlea visualization
            with ui.card().classes('w-full'):
                ui.label('Cochlear Frequency Response').classes('text-h6')
                
                freq_demo_slider = ui.slider(min=20, max=20000, value=1000)
                ui.label().bind_text_from(freq_demo_slider, 'value', lambda v: f'Frequency: {v:.0f} Hz')
                
                cochlea_plot = ui.card().classes('w-full')
                
                def update_cochlea_plot():
                    with cochlea_plot:
                        cochlea_plot.clear()
                        
                        with ui.matplotlib(figsize=(8, 3)).figure as fig:
                            
                            ax = fig.add_subplot(111)
                            
                            # Create cochlea shape (simplified)
                            theta = np.linspace(0, 4*np.pi, 1000)
                            r = 1 - 0.1 * theta
                            x = r * np.cos(theta)
                            y = r * np.sin(theta)
                            
                            # Plot cochlea
                            ax.plot(x, y, 'k-', linewidth=2)
                            
                            # Calculate response location (simplified model)
                            freq = freq_demo_slider.value
                            # Log scale mapping from 20Hz-20kHz to cochlea length
                            pos = 1 - np.log(freq/20) / np.log(20000/20)
                            pos = min(1, max(0, pos)) * 4 * np.pi
                            
                            # Find nearest point on cochlea
                            idx = np.argmin(np.abs(theta - pos))
                            response_x, response_y = x[idx], y[idx]
                            
                            # Highlight response area
                            ax.plot(response_x, response_y, 'ro', markersize=10)
                            
                            # Annotations
                            ax.annotate('Base\n(High Freq)', xy=(1, 0), xytext=(1.2, 0), 
                                        arrowprops=dict(arrowstyle='->'))
                            ax.annotate('Apex\n(Low Freq)', xy=(x[-1], y[-1]), xytext=(x[-1]-0.5, y[-1]-0.3), 
                                        arrowprops=dict(arrowstyle='->'))
                            ax.annotate(f'{freq} Hz', xy=(response_x, response_y), 
                                        xytext=(response_x + 0.3, response_y + 0.3),
                                        arrowprops=dict(arrowstyle='->'))
                            
                            ax.set_title('Simplified Cochlear Frequency Response')
                            ax.set_xlim(-1.5, 1.5)
                            ax.set_ylim(-1.5, 1.5)
                            ax.set_aspect('equal')
                            ax.axis('off')
                            
                            fig.tight_layout()
                
                freq_demo_slider.on('update:model-value', update_cochlea_plot)
                
                # Initial plot
                update_cochlea_plot()
        
        with ui.tab_panel(connections_tab):
            ui.markdown('''
            ## Making Connections
            
            This section explores how the physics of sound connects to our perception.
            
            ### Frequency and Pitch
            
            - **Physical Property**: Frequency (Hz)
            - **Perception**: Pitch (high/low)
            - **Connection**: Higher frequencies create higher pitches through faster basilar membrane vibrations
            
            ### Amplitude and Loudness
            
            - **Physical Property**: Amplitude/Intensity
            - **Perception**: Loudness/Volume
            - **Connection**: Greater amplitudes cause stronger hair cell responses, perceived as louder sounds
            
            ### Complex Waves and Timbre
            
            - **Physical Property**: Harmonic content/waveform shape
            - **Perception**: Timbre/sound quality
            - **Connection**: Different instruments playing the same note have different harmonic structures
            
            ### Experiment with the Generator Tab
            
            Try these experiments in the Generator tab:
            
            1. Create sounds with the same frequency but different waveforms to hear differences in timbre
            2. Generate a 440 Hz tone (A4) and then 880 Hz (A5) to hear the octave relationship
            3. Try extreme frequencies (very low or high) to test your hearing range
            ''')


# Main application
def sound_explorer():
    ui.label('Sound Explorer').classes('text-h3')
    ui.markdown('''
    ## Interactive Sound Physics Lab
    Explore the properties of sound waves by visualizing, creating, and manipulating audio.
    ''')
    
    # Create tabs for different functionalities
    with ui.tabs().classes('w-full') as tabs:
        visualize_tab = ui.tab('Visualize Sound')
        generate_tab = ui.tab('Generate Sound')
        learn_tab = ui.tab('Learn More')
    
    with ui.tab_panels(tabs, value=visualize_tab).classes('w-full'):
        with ui.tab_panel(visualize_tab):
            setup_visualization_tab()
        
        with ui.tab_panel(generate_tab):
            setup_generator_tab()
            
        with ui.tab_panel(learn_tab):
            setup_learning_tab()

# Start the application
sound_explorer()
ui.run()
