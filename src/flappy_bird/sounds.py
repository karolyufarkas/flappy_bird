"""Sound functions for Flappy Bird"""

import pygame

# Since pygame.sndarray might not be available, create a fallback
try:
    # Check if pygame.mixer is available
    if not hasattr(pygame, 'mixer') or not pygame.mixer.get_init():
        # Define dummy sound objects if mixer is not available
        class DummySound:
            def play(self): pass
        flap_sound = DummySound()
        hit_sound = DummySound()
        point_sound = DummySound()
    else:
        import numpy
        # Create more complex sound effects programmatically
        def create_flap_sound():
            """Create a more complex flap sound effect"""
            sample_rate = 22050
            duration_ms = 120
            n_samples = int(round(duration_ms * sample_rate / 1000.0))

            # Generate samples for stereo (2 channels)
            arr = numpy.zeros((n_samples, 2))
            for i in range(n_samples):
                t = float(i) / sample_rate

                # Create a combination of frequencies that decrease over time
                freq1 = 523.25 * (1 - t / (duration_ms/1000))  # Decreasing C note
                freq2 = 659.25 * (1 - t / (duration_ms/1000))  # Decreasing E note

                # Create a more complex waveform combining multiple harmonics
                val = 0.3 * numpy.sin(2 * numpy.pi * freq1 * t)
                val += 0.2 * numpy.sin(2 * numpy.pi * freq2 * t)
                val += 0.1 * numpy.sin(2 * numpy.pi * freq1 * 2 * t)  # Harmonic
                val += 0.1 * numpy.sin(2 * numpy.pi * freq2 * 1.5 * t)  # Harmonic

                # Apply envelope to make it sound more natural
                envelope = 1.0 - (t / (duration_ms/1000)) ** 2  # Quadratic fade
                val *= envelope

                val *= 0.3 * 32767.0  # Volume control
                arr[i][0] = val  # Left channel
                arr[i][1] = val  # Right channel

            # Convert to int16 and create sound
            arr = arr.astype(numpy.int16)
            sound = pygame.sndarray.make_sound(arr)
            return sound

        def create_hit_sound():
            """Create a more complex hit sound effect"""
            sample_rate = 22050
            duration_ms = 400
            n_samples = int(round(duration_ms * sample_rate / 1000.0))

            # Generate samples for stereo (2 channels)
            arr = numpy.zeros((n_samples, 2))
            for i in range(n_samples):
                t = float(i) / sample_rate

                # Create a noise-like sound with multiple decreasing frequencies
                total_val = 0
                for harmonic in range(1, 5):
                    freq = 220.00 / harmonic * (1 - t / (duration_ms/1000))  # Decreasing frequency
                    total_val += numpy.sin(2 * numpy.pi * freq * t) / harmonic

                # Add some white noise for impact
                noise_factor = numpy.random.uniform(-0.1, 0.1) * (1 - t / (duration_ms/1000))
                total_val += noise_factor

                # Apply envelope for realistic decay
                envelope = numpy.exp(-t * 3)  # Exponential decay
                total_val *= envelope

                total_val *= 0.5 * 32767.0  # Volume control
                arr[i][0] = total_val  # Left channel
                arr[i][1] = total_val  # Right channel

            # Convert to int16 and create sound
            arr = arr.astype(numpy.int16)
            sound = pygame.sndarray.make_sound(arr)
            return sound

        def create_point_sound():
            """Create a more complex point sound effect"""
            sample_rate = 22050
            duration_ms = 200
            n_samples = int(round(duration_ms * sample_rate / 1000.0))

            # Generate samples for stereo (2 channels)
            arr = numpy.zeros((n_samples, 2))
            for i in range(n_samples):
                t = float(i) / sample_rate

                # Create a pleasant arpeggiated sound
                freq1 = 523.25  # C note
                freq2 = 659.25  # E note
                freq3 = 783.99  # G note

                # Play notes in sequence
                note_duration = (duration_ms/1000) / 3
                if t < note_duration:
                    val = numpy.sin(2 * numpy.pi * freq1 * t)
                elif t < 2 * note_duration:
                    val = numpy.sin(2 * numpy.pi * freq2 * t)
                else:
                    val = numpy.sin(2 * numpy.pi * freq3 * t)

                # Apply envelope for clean attack and decay
                attack_time = 0.02  # 20ms attack
                release_time = 0.1  # 100ms release
                if t < attack_time:
                    envelope = t / attack_time  # Linear attack
                elif t > (duration_ms/1000 - release_time):
                    envelope = (duration_ms/1000 - t) / release_time  # Linear release
                else:
                    envelope = 1.0  # Sustain

                val *= envelope
                val *= 0.4 * 32767.0  # Volume control
                arr[i][0] = val  # Left channel
                arr[i][1] = val  # Right channel

            # Convert to int16 and create sound
            arr = arr.astype(numpy.int16)
            sound = pygame.sndarray.make_sound(arr)
            return sound

        # Initialize sounds
        if pygame.sndarray.get_arraytype() != 'numpy':
            raise ImportError("sndarray not available")
        flap_sound = create_flap_sound()
        hit_sound = create_hit_sound()
        point_sound = create_point_sound()
        
except (ImportError, AttributeError, NotImplementedError):
    # Fallback if numpy, sndarray, or mixer isn't available
    class DummySound:
        def play(self): pass
    flap_sound = DummySound()
    hit_sound = DummySound()
    point_sound = DummySound()