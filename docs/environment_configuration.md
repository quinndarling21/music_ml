# Environment Configuration Documentation

## Overview
This document explains how the environment configuration works across development and production environments for both the frontend React application and backend Flask API.

## Frameworks and Technologies

### Frontend
- **React**: Main frontend framework
- **Material-UI**: Component library for styling
- **Axios**: HTTP client for API requests
- **Express**: Production server for static file serving
- **React Router**: Client-side routing

### Backend
- **Flask**: Main backend framework
- **Flask-SQLAlchemy**: Database ORM
- **Flask-Session**: Session management
- **Flask-CORS**: Cross-Origin Resource Sharing
- **PostgreSQL**: Production database
- **SQLite**: Development database
- **Redis**: Session storage (production)

## Environment Detection & Configuration

### Development Environment
- Uses local SQLite database
- Less strict CORS and cookie settings
- React development server with hot reloading
- Local environment variables via .env files
- Debug logging enabled
- Session stored in SQLite

### Production Environment
- Uses PostgreSQL database
- Strict security settings
- Express server for static file serving
- Environment variables set in Heroku
- Production-level logging
- Session stored in Redis

## URI Configuration

### Development URIs
- Frontend: http://127.0.0.1:3000
- Backend: http://127.0.0.1:5000
- Database: SQLite file (dev.db)
- Callback: http://127.0.0.1:5000/api/auth/callback

### Production URIs
- Frontend: https://musaic-frontend-7a12a4566f21.herokuapp.com
- Backend: https://musaic-backend-3d46a4f2ff11.herokuapp.com
- Database: Heroku PostgreSQL
- Callback: https://musaic-backend-3d46a4f2ff11.herokuapp.com/api/auth/callback

## Database Configuration

### Development
- Uses SQLite for simplicity
- Automatically creates database file
- No additional setup required
- Tables created on application start

### Production
- Uses Heroku PostgreSQL
- Connection string provided by Heroku
- Automatic SSL configuration
- Connection pooling enabled

## Session Management

### Development
- Less strict cookie settings
- SQLAlchemy session interface
- Local session storage
- Debug-friendly configuration

### Production
- Secure cookie settings
- Redis session storage
- Cross-domain support
- Strict security headers

## Environment Variables

### Required Variables
1. Spotify Configuration
   - Client ID
   - Client Secret
   - Redirect URI
   - Frontend URL

2. Flask Configuration
   - Secret Key
   - Environment
   - Debug Mode
   - Database URL

3. Frontend Configuration
   - API URL
   - Port
   - Node Environment

## Security Considerations

### Development
- CORS allows localhost origins
- HTTP allowed
- Debug mode enabled
- Less strict cookie policies

### Production
- CORS restricted to specific domains
- HTTPS required
- Debug mode disabled
- Strict cookie policies
- Security headers enabled

## Deployment Process

### Frontend Deployment
1. Environment Detection
2. Build Process
3. Static File Serving
4. Environment Variables
5. Domain Configuration

### Backend Deployment
1. Database Migration
2. Environment Configuration
3. Service Configuration
4. Security Settings
5. Logging Setup

## Troubleshooting Guide

### Common Issues
1. Database Connection
   - Check environment
   - Verify credentials
   - Check connection string

2. Authentication Flow
   - Verify callback URLs
   - Check session configuration
   - Validate CORS settings

3. Environment Variables
   - Check loading order
   - Verify configuration
   - Validate values

### Logging and Monitoring
1. Development Logging
   - Console output
   - Debug messages
   - Local log files

2. Production Logging
   - Heroku logs
   - Error tracking
   - Performance monitoring

## Maintenance

### Regular Tasks
1. Database maintenance
2. Session cleanup
3. Log rotation
4. Security updates
5. Dependency updates

### Backup Procedures
1. Database backups
2. Configuration backups
3. Environment variable management
4. Recovery procedures

## Future Considerations
1. Scaling strategies
2. Performance optimization
3. Security enhancements
4. Monitoring improvements
5. Deployment automation