# Dashview

**Dashview** is a personal project that I developed in order to automate certain home  functionalities. The software is actually deployed on a **Raspberry Pi 4** with Raspberry OS.

It is based on a web application designed for smart home automation, allowing users to control and monitor several home functions, such as the boiler, temperature/pressure sensors and waste management. The application provides an intuitive, multi-language interface with real-time communication between the backend and frontend.

![Immagine 2024-10-10 123324](https://github.com/user-attachments/assets/0ce405d5-b4ab-4521-a13e-5126d8b1e8b6)

---

## Key Features

- **Boiler Control**: Easily manage your home's heating system. Start the heater for a custom time and receive real-time remaining time data.
- **Temperature and Pressure Sensors**: Monitor environmental conditions such as temperature and pressure in real-time.
- **Waste Management**: Automatically track and manage waste collection schedules, retrieving information directly from trash company site.
- **Real-Time Communication**: Built on SocketIO, utilizing WebSockets for event-driven communication between the client and server.
- **Multi-language Support**: Interface localization provided via i18n. The language will be detected through browser language settings.
- **Find My Phone**: A button that, when clicked, will make your phone ring (if connected to the same Wi-Fi network), helping you locate it quickly. Needs a server installed on the smartphone
- **Mobile Access**: Use Dashview through your smartphone without using the Raspberry screen mounted on the wall

## Architecture Overview

Dashview is divided into two main components:

1. **Backend**:
   - Written in Python, with **FastAPI**.
   - Virtual environment management handled by **Poetry**.
   - Communicates with a **MongoDB** database (running in a separate container) to store waste collection data retrieved from the official trash management website.
   - Real-time event-based communication using **SocketIO**.

2. **Frontend**:
   - Built with **Vue.js**, using **Vuetify** for UI components and **TypeScript** for type safety.
   - Provides a responsive, multi-language interface.


### Communication

The backend and frontend communicate through **SocketIO**, enabling seamless real-time updates and event-based interactions between the client and server.

## Tech Stack

- **Backend**: Python, SocketIO, MongoDB
- **Frontend**: Vue.js, Vuetify, TypeScript, i18n for localization
- **Containerization**: Docker (separate Dockerfiles for backend and frontend)

## TODO

There are various functionalities that I want to develop, here's some:

- **Lights management**: show a top view house plan showing all the lights available. Once selected a light, the user can control intensity and color. Could use Hue bridge or dicrect bluetooth communication between Raspberry and the light bulb
- **Roomba Commands**: Start and stop roomba from Dashview. Will use an arduino nano attached to the robot with bluetooth module that receive commands from Raspberry and communicate through the Roomba's serial port
- **Google Calendar Events**: Show next events/birthdays gathering data from Google Calendar
- **Automatic Roller Shutter**: Close certain (or all) roller shutter that have an electric motor. This could be done via manual command or via schedule, for example the system could close all the roller shutter at midnight.

