# Smart Energy Meter - Frontend

This is the frontend application for the Smart Energy Meter Monitoring System. It provides a real-time dashboard for visualizing energy consumption, forecasting usage, and interacting with an AI-powered "Energy Boss" chatbot.

## 🛠 Tech Stack

- **Framework**: [Next.js 15+](https://nextjs.org/) (App Router)
- **Styling**: [Tailwind CSS 4](https://tailwindcss.com/)
- **Icons**: [Lucide React](https://lucide.dev/)
- **Charts**: [Recharts](https://recharts.org/)
- **Animations**: [Framer Motion](https://www.framer.com/motion/)
- **API Client**: [Axios](https://axios-http.com/)

## 🚀 Key Features

- **Real-time Data Dashboard**: Live visualization of voltage, current, and power.
- **Energy Forecasting**: 7-day and 30-day usage predictions with interactive charts.
- **Anomaly Detection List**: View historical and real-time anomalies detected by the system.
- **AI Chatbot**: "Energy Boss" persona for answering energy-related queries.
- **Responsive Design**: Fully optimized for mobile and desktop viewing.

## ⚙️ Getting Started

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Configure environment (Optional)**:
   Ensure the backend is running at `http://localhost:8000` (default) or update the API service configuration in `services/api.ts`.

3. **Run the development server**:
   ```bash
   npm run dev
   ```

4. **Build for production**:
   ```bash
   npm run build
   ```

## 📂 Folder Structure

- `app/`: Contains the main pages and layouts (Dashboard, Chat, Forecast, Anomalies).
- `components/`: Reusable UI components (StatCards, Charts, Navbar, DeviceCards).
- `services/`: API integration and data fetching logic.
- `public/`: Static assets.

## 📄 License

MIT License
