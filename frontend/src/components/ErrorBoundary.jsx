/**
 * Error Boundary component for catching React errors
 */
import { Component } from 'react';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    this.setState({ error, errorInfo });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-container" style={{ minHeight: '80vh' }}>
          <div className="glass-card" style={{ maxWidth: '480px', textAlign: 'center' }}>
            <div className="error-icon">❌</div>

            <h2 className="page-title" style={{ marginBottom: '0.5rem' }}>
              Something went wrong
            </h2>

            <p className="error-message" style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
              We're sorry, but something unexpected happened. Please try refreshing the page.
            </p>

            {import.meta.env.DEV && this.state.error && (
              <details style={{
                marginTop: '1rem',
                padding: '1rem',
                background: 'var(--bg-tertiary)',
                borderRadius: 'var(--radius-sm)',
                textAlign: 'left',
                fontSize: '0.8rem',
              }}>
                <summary style={{ cursor: 'pointer', fontWeight: 600, marginBottom: '8px' }}>
                  Error Details
                </summary>
                <pre style={{ color: 'var(--error)', overflow: 'auto', fontSize: '0.75rem' }}>
                  {this.state.error.toString()}
                  {this.state.errorInfo && this.state.errorInfo.componentStack}
                </pre>
              </details>
            )}

            <button
              onClick={() => window.location.reload()}
              className="btn btn-primary"
              style={{ marginTop: '1.5rem' }}
            >
              🔄 Refresh Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
