# MechLocator 🚗🔧

A comprehensive web-based application that helps users discover nearby mechanic shops with real-time location services, Google Maps integration, and instant contact capabilities.

## 🌟 Features

### Core Functionality
- **Real-time Location Detection**: Automatically detect user location using browser geolocation API
- **Nearby Mechanic Discovery**: Find mechanic shops within customizable radius (1km, 5km, 10km, 15km)
- **Google Maps Integration**: Interactive map interface with mechanic markers and user location
- **One-Click Calling**: Direct phone calls to mechanics using 'tel:' URI scheme
- **Smart Filtering**: Filter by distance, rating, and availability
- **Rating System**: 5-star rating system for mechanic shops

### User Experience
- **Responsive Design**: Mobile-first design that works on all devices
- **Modern UI**: Beautiful, intuitive interface built with Bootstrap 5
- **Fast Performance**: Optimized queries and efficient data handling
- **Accessibility**: WCAG compliant with proper ARIA labels and keyboard navigation

### Admin Features
- **Comprehensive Dashboard**: Full CRUD operations for mechanic shops
- **User Management**: Admin panel for user accounts and profiles
- **Activity Logging**: Track user actions and search queries
- **Image Upload**: Support for shop photos and branding

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7 (Python web framework)
- **Database**: SQLite (easily upgradeable to PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5.3.0
- **Maps**: Google Maps JavaScript API
- **Icons**: Font Awesome 6.4.0
- **Forms**: Django Crispy Forms with Bootstrap 5
- **Geolocation**: Geopy for distance calculations

## 📋 Requirements

- Python 3.8+
- Django 4.2.7
- Google Maps API Key
- Modern web browser with geolocation support

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Vijayapardhu/mechlocator.git
cd mechlocator
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
cp .env
# Edit .env file with your configuration
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Collect Static Files
```bash
python manage.py collectstatic
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## ⚙️ Configuration

### Google Maps API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Maps JavaScript API
4. Create API key
5. Add the key to your `.env` file:
   ```
   GOOGLE_MAPS_API_KEY=your-api-key-here
   ```

### Environment Variables
Key environment variables in `.env`:
- `SECRET_KEY`: Django secret key for security
- `DEBUG`: Set to False in production
- `GOOGLE_MAPS_API_KEY`: Your Google Maps API key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## 📱 Usage

### For Users
1. **Homepage**: Visit the main page to start searching
2. **Location Access**: Allow location access or manually set location
3. **Search Filters**: Choose radius and minimum rating
4. **Browse Results**: View mechanic shops on map and in list
5. **Contact Mechanics**: Use "Call Now" button for instant contact
6. **View Details**: Click on mechanic cards for detailed information

### For Administrators
1. **Admin Panel**: Access `/admin/` with superuser credentials
2. **Manage Mechanics**: Add, edit, and delete mechanic shops
3. **User Management**: Monitor user accounts and activity
4. **Analytics**: View search queries and user behavior logs

## 🗄️ Database Models

### Mechanic
- Basic info (name, address, contact)
- Location coordinates (latitude, longitude)
- Rating and working hours
- Shop images and status

### User
- Authentication and profile information
- Extended profile with phone and address
- Activity tracking and preferences

### ActivityLog
- User action logging
- Search queries and results
- Call tracking and analytics

## 🔧 API Endpoints

- `POST /api/search/`: Search for nearby mechanics
- `POST /api/log-call/`: Log mechanic calls
- All endpoints support CSRF protection and proper authentication

## 🎨 Customization

### Styling
- Modify `static/css/style.css` for custom styles
- Update Bootstrap variables in CSS custom properties
- Add custom animations and transitions

### Templates
- All templates are in `templates/` directory
- Base template provides consistent layout
- Easy to modify and extend

### JavaScript
- Main functionality in `static/js/main.js`
- Modular design for easy customization
- Utility functions for common operations

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in environment
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set up static file serving (nginx/Apache)
- [ ] Configure HTTPS with SSL certificates
- [ ] Set up proper logging and monitoring
- [ ] Configure backup strategies

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "mechlocator.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Environment Variables for Production
```bash
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
GOOGLE_MAPS_API_KEY=your-production-api-key
```

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Test Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📊 Performance

### Optimization Features
- Database query optimization with select_related
- Efficient distance calculations using Geopy
- Lazy loading of images and content
- Responsive image handling
- Caching strategies for static content

### Monitoring
- Activity logging for user behavior analysis
- Search query tracking for performance insights
- Error logging and monitoring
- Performance metrics collection

## 🔒 Security

### Security Features
- CSRF protection on all forms
- SQL injection prevention with Django ORM
- XSS protection with template escaping
- Secure password hashing
- Session security configuration
- Input validation and sanitization

### Best Practices
- Regular security updates
- Environment variable management
- HTTPS enforcement in production
- Rate limiting for API endpoints
- Input validation and sanitization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add tests for new features
- Update documentation as needed
- Ensure accessibility compliance

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django community for the excellent web framework
- Bootstrap team for the responsive UI framework
- Google Maps team for the mapping API
- Font Awesome for the icon library
- All contributors and users of MechLocator

## 📞 Support

- **Documentation**: [Wiki](https://github.com/yourusername/mechlocator/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/mechlocator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/mechlocator/discussions)
- **Email**: support@mechlocator.com

## 🔮 Future Enhancements

- [ ] Online appointment booking system
- [ ] Push notifications for updates
- [ ] User reviews and ratings
- [ ] AI-based recommendations
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Integration with automotive services

---

**MechLocator** - Connecting drivers with trusted mechanics since 2024 🚗🔧

*Built with ❤️ using Django and modern web technologies*
