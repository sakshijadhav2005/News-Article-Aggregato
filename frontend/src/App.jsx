import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import ErrorBoundary from './components/ErrorBoundary';
import HomePage from './pages/HomePage';
import ArticlesPage from './pages/ArticlesPage';
import ArticleDetailPage from './pages/ArticleDetailPage';
import ClustersPage from './pages/ClustersPage';
import AdminPage from './pages/AdminPage';
import './index.css';

function App() {
  return (
    <ErrorBoundary>
      <Router
        future={{
          v7_startTransition: true,
          v7_relativeSplatPath: true,
        }}
      >
        <div className="app-container">
          <Navbar />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/articles" element={<ArticlesPage />} />
              <Route path="/articles/:id" element={<ArticleDetailPage />} />
              <Route path="/clusters" element={<ClustersPage />} />
              <Route path="/clusters/:clusterId" element={<ClustersPage />} />
              <Route path="/admin" element={<AdminPage />} />
              <Route path="*" element={
                <div className="empty-container">
                  <div className="empty-icon">🔍</div>
                  <h2 className="page-title">Page Not Found</h2>
                  <p className="empty-message">The page you're looking for doesn't exist.</p>
                </div>
              } />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
