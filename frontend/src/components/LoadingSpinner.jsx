/**
 * Reusable loading spinner component
 */
const LoadingSpinner = ({ message = 'Loading...' }) => {
  return (
    <div className="loading-container">
      <div className="loading-spinner"></div>
      {message && (
        <p className="loading-text">{message}</p>
      )}
    </div>
  );
};

export default LoadingSpinner;
