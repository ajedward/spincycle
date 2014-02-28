spincycle
=========

spincycle is a school research project that should emulate turntable DJ / scratching techniques using pyo and wxpython.

Author: Andrew Edwards
Contact: ajedward@gmail.com

This package consists of main.py and turntable.py.  main launches two turntables side by side.
Here are a few of the turntable features (in development, planned features are marked 'TODO') :
  - Start/stop functionality (bouton moteur) DONE
    TODO: add an 'ease' feature such that it can stop and start as a turntable would.
  - Rotating turntables at 33 1/3 RPM (DONE).
  - Virtual vinyl album "stops" when there is a mouse down on the album. DONE
  - Motion of the virtual vinyl album when there is a drag on the Y axis DONE (rudimentary)
    TODO: capture the position on the album and act accordingly (Y axis inverted on right 
          side, X axis also accordingly rotates when the pointer is above or below the 
          center of the virtual vinyl.
  - TODO: Upload samples in WAV, AIF, etc. formats to populate each vinyl album.
  - TODO: Faders and Crossfader module (middle portion of UI between turntables)
  - TODO: Granular sampling engine that allows control of the position in the sample 
          and the frequency depending on the manipulation of the virtual vinyl album.
  - TODO: Control of the 'sharpness' or sensitivity of the crossfade control.

