# Project Overview: Wedding Band Song Request App

## Project Aim

The Wedding Band Song Request App is designed to enhance the live event experience by simplifying the process of song requests. Instead of guests approaching the band in person to request songs, this application allows guests to scan a QR code at an event and submit their song requests digitally. This streamlines the process for both guests and bands, creating a more interactive and enjoyable experience.

## Key Features

### For Guests

- **QR Code Scanning**: Guests can scan a QR code placed at their table or around the venue to access the song request app.
- **Song Request Submission**: Once in the app, guests can search for and request their favourite songs to be played during the event.
- **Dedication Message**: Guests have the option to include a personal dedication with their song request, making their requests more special.
- **Real-Time Status Updates**: Guests receive live updates on the status of their song requests, informing them whether their song has been accepted and when it will be played.
- **OAuth2 Authentication**: Guests can log in using OAuth2 providers (e.g., Google, Facebook) for a streamlined and secure sign-in process.

### For Bands

- **Event Management**: Bands can create and manage multiple events through the app, specifying details such as event name, location, and schedule.
- **QR Code Generation**: Bands can generate unique QR codes for each event, which can be placed on tables or other locations at the venue.
- **Song Request Dashboard**: Bands can view incoming song requests in real-time, accept or reject them, and manage their playlist accordingly.
- **Analytics and Reporting**: Bands can access analytics on song requests and guest interactions to improve future events.
- **OAuth2 Authentication**: Bands can use OAuth2 providers to log in securely, simplifying access and ensuring secure management of their events.

## Workflow

1. **Event Setup**:
   - Bands create and configure their events within the app.
   - QR codes are generated and distributed to be placed at various locations around the venue.

2. **Guest Interaction**:
   - Guests scan the QR code using their mobile devices to access the song request app.
   - Guests log in using OAuth2 providers for a secure and convenient sign-in experience.
   - Guests search for and submit their song requests, optionally including dedication messages.
   - The app provides real-time status updates on the requests.

3. **Band Interaction**:
   - Bands log in using OAuth2 providers for secure access to the app.
   - Bands monitor the song request dashboard to view and manage incoming requests.
   - Requests are accepted or rejected based on the band’s preferences and availability.
   - Bands use analytics to gain insights into guest preferences and improve future events.

## Technologies Used

- **Backend**: Flask (Python) for handling API requests and managing application logic.
- **Database**: PostgreSQL for storing user data, song requests, event details, and more.
- **Frontend**: React.js for building an interactive and responsive user interface.
- **Authentication**: OAuth2 for secure and streamlined user authentication and authorisation.

## Benefits

- **For Guests**: A seamless and engaging way to request songs without interrupting the band or event, with secure and convenient authentication via OAuth2.
- **For Bands**: Streamlined management of song requests and event organisation, with real-time updates, detailed analytics, and secure access using OAuth2.

## Conclusion

The Wedding Band Song Request App aims to revolutionise the live event experience by integrating technology to facilitate song requests and improve guest interaction. By allowing guests to request songs via QR codes and providing bands with efficient management tools and secure OAuth2 authentication, the app enhances the overall enjoyment and security of live events.
