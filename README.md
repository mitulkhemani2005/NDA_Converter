# BharatDocs - NDA Converter

A full-stack PDF document processing application that allows users to upload, process, and download PDF documents. Built for **New Durga Agencies, Ujjain**.

**Live Demo:** [nda-converter.vercel.app](https://nda-converter.vercel.app)

---

## Features

- **PDF Upload** - Drag and drop or click to upload PDF documents
- **PDF Processing** - Extract, modify, and translate text within PDFs
- **Download Processed PDFs** - Get your modified documents instantly
- **Translation Support** - Region-based text translation capabilities
- **Fast & Responsive** - Modern frontend with seamless user experience

---

## Tech Stack

### Frontend
- **TypeScript** (91.9%)
- **CSS** (4.0%)
- **JavaScript** (0.1%)

### Backend
- **Python** (4.0%)
- **Flask** - Web framework for API endpoints

### Key Python Modules
| Module | Description |
|--------|-------------|
| `pdf_reader.py` | PDF reading utilities |
| `pdf_modifier.py` | PDF modification tools |
| `pdf_text_extractor.py` | Text extraction from PDFs |
| `region_text_extractor.py` | Region-based text extraction |
| `region_translator.py` | Translation for specific regions |
| `translator.py` | General translation functionality |

---

## Project Structure

```
NDA_Converter/
├── frontend/                    # Frontend application (TypeScript)
├── fonts/                       # Custom fonts for PDF generation
├── uploads/                     # Uploaded PDF storage
├── app.py                       # Main Flask application
├── config.json                  # Configuration settings
├── config_loader.py             # Configuration loader utility
├── pdf_modifier.py              # PDF modification logic
├── pdf_reader.py                # PDF reading utilities
├── pdf_text_extractor.py        # Text extraction module
├── region_text_extractor.py     # Region-based extraction
├── region_translator.py         # Region translation
├── translator.py                # Translation module
├── requirements.txt             # Python dependencies
└── runtime.txt                  # Python runtime version
```

---

## Getting Started

### Prerequisites

- Python 3.x
- Node.js (for frontend)

### Backend Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mitulkhemani2005/NDA_Converter.git
   cd NDA_Converter
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload a PDF file |
| `GET` | `/download/<filename>` | Download processed PDF |
| `POST` | `/process` | Process uploaded PDF |

---

## Configuration

The application uses `config.json` for configuration settings. Update this file to customize:

- Upload directory paths
- Translation settings
- PDF processing options

---

## Deployment

This application is deployed on **Vercel**. 

Visit the live version at [nda-converter.vercel.app](https://nda-converter.vercel.app).

### Deploy Your Own

1. Fork this repository
2. Connect your fork to Vercel
3. Configure environment variables (if any)
4. Deploy

---

## Author

**Mitul Khemani**

- GitHub: [@mitulkhemani2005](https://github.com/mitulkhemani2005)

Made for **New Durga Agencies, Ujjain**

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Acknowledgments

- Flask for the backend framework
- Vercel for hosting
- All contributors and users of this project
