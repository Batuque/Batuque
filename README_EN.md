# Batuque

The Batuque project is an application that uses computer vision to detect colors in real-time through the camera and play percussion instrument sounds based on the detected colors. The graphical interface is managed with the Pygame library, providing an interactive home screen and configuration menus.

## 🔨 Project Features

- **Color Detection:** Detects specific colors in the camera image using the HSV color space and applies masks to identify these colors.
- **Sound Playback:** Plays percussion instrument sounds when the corresponding color is detected in predefined regions of interest (ROIs).
- **Image Overlay:** Displays transparent images over the detected regions to visually represent the instruments.
- **Graphical Interface:** Provides a home screen with control buttons, a settings menu, and a loading screen.
- **Volume and Resolution Control:** Allows adjusting the music volume and screen resolution through the settings menu.

### Visual Example of the Project

![Screenshot 2024-08-11 211550](https://github.com/user-attachments/assets/a8d3dca2-70ed-4246-8350-34b1ec0b187b)
![Screenshot 2024-08-11 225320](https://github.com/user-attachments/assets/e3ebd3e8-0319-49c8-b83f-d77ef9b7bf95)
![image](https://github.com/user-attachments/assets/c1a1b929-dbf9-4468-a144-8868e009d5ed)

## ✔️ Techniques and Technologies Used

- **OpenCV:** For video capture and image processing, including color detection and image overlay.
- **Pygame:** For creating the graphical interface, managing events, and playing sounds.
- **Python:** Programming language used to develop the application.

## 📁 Project Structure

- `screens/`
    - `menu_resolution.py`: Script for setting the screen resolution.
    - `menu_volume.py`: Script for adjusting the audio volume.
    - `login_screen.py`: Script for the login screen.
    - `registration_screen.py`: Script for the registration screen.
- `src/`
    - `Images/`: Contains images used in the graphical interface.
    - `sounds/`: Contains audio files for the instruments.
    - `batuque.py`: Main script that performs color detection and sound playback.
    - `interface.py`: Manages the graphical interface with Pygame, including the home screen and menus.
- `.gitignore`: File specifying which files and directories should be ignored by Git.
- `LICENSE`: Project license file.
- `README.md`: Project documentation.
- `requirements.txt`: Lists the project dependencies.
- `run_batuque.py`: Script to run the Batuque project.
- `test_target_color.py`: Script to test color detection.

## 🌐 Deploy

To run the project locally, follow these steps:

1. **Install Dependencies:**
   Run the command `pip install -r requirements.txt` to install the necessary dependencies.

2. **Prepare Resources:**
   Ensure that the images and sounds are in the `src/Images` and `src/sounds` directories, respectively.

3. **Run the Project:**
   Run the `interface.py` script to start the application.
