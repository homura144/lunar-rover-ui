# Lunar Rover UI

An Electron application with Vue and TypeScript

## Recommended IDE Setup

- [VSCode](https://code.visualstudio.com/) + [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint) + [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin)

## Development Platform

- Raspberry Pi OS 5B

## Installation

### Clone the Repository

```sh
git clone git@github.com:homura144/lunar-rover-ui.git
cd lunar-rover-ui
```

### Setting up Environment

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution).

2. Install npm and node:

    ```sh
    sudo apt update
    sudo apt install nodejs npm
    ```

3. Install yarn:

    ```sh
    npm install --global yarn
    ```

4. Create a new conda environment:

    ```sh
    conda create --name lunar-rover python=3.10
    ```

5. Activate the conda environment:

    ```sh
    conda activate lunar-rover
    ```

6. Install the required pip packages:

    ```sh
    pip install -r requirements.txt
    ```

7. Install all Node.js dependencies:

    ```sh
    yarn
    ```

## Running the Application

1. Activate the conda environment:

    ```sh
    conda activate lunar-rover
    ```

2. Start the Electron application:

    ```sh
    yarn start
    ```

3. Modify constant values in `src/share/constants.ts` if necessary

## File Structure

```plaintext
lunar-rover-ui/
├── src/
│   ├── main/                # Contains the main process code for Electron
│   │   └── index.ts         # Main entry point for Electron
│   ├── renderer/            # Contains the renderer process code, including Vue components
│   │   ├── App.vue          # Vue root component
│   │   ├── main.ts          # Vue entry point
│   │   └── ...              
│   ├── share/               # Contains shared code and constants
│   │   ├── constants.ts     # Shared constants
│   │   └── ...              
│   ├── python/              # Python scripts for hardware
│   │   └── ...              
│   └── ...                  
└── ...                      
```
