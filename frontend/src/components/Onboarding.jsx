import { useState } from 'react';
import PropTypes from 'prop-types';
import { createContext } from '../api';

function Onboarding({ onComplete }) {
  const [formData, setFormData] = useState({
    company_size: '',
    industry: '',
    pain_points: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.company_size || !formData.industry || !formData.pain_points) {
      setError('Please fill in all fields.');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const newConversation = await createContext(formData);
      onComplete(newConversation, formData);
    } catch (err) {
      console.error(err);
      setError('Failed to start conversation. Ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="onboarding-container animate-fade-in">
      <div className="onboarding-card glass-panel" role="region" aria-label="Onboarding Form">
        <h1>Welcome to Aura.</h1>
        <p>Your AI Sales Assistant for the Enterprise AI Productivity Suite. Tell us a bit about your organization to get started.</p>
        
        {error && (
          <div 
            className="error-alert" 
            style={{ 
              backgroundColor: 'rgba(239, 68, 68, 0.1)', 
              border: '1px solid var(--danger)', 
              borderRadius: 'var(--radius-md)',
              padding: '1rem',
              color: 'var(--danger)', 
              marginBottom: '1.5rem', 
              fontSize: '0.9rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }} 
            role="alert"
            aria-live="assertive"
          >
            <span aria-hidden="true">⚠️</span>
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="company_size">Company Size</label>
            <select 
              id="company_size" 
              name="company_size" 
              value={formData.company_size} 
              onChange={handleChange}
              aria-required="true"
            >
              <option value="">Select size...</option>
              <option value="1-50">1-50 employees</option>
              <option value="51-200">51-200 employees</option>
              <option value="201-1000">201-1000 employees</option>
              <option value="1000+">1000+ employees</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="industry">Industry</label>
            <input 
              type="text" 
              id="industry" 
              name="industry" 
              placeholder="e.g. Healthcare, Finance, SaaS..." 
              value={formData.industry} 
              onChange={handleChange}
              aria-required="true"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="pain_points">Current Pain Points</label>
            <textarea 
              id="pain_points" 
              name="pain_points" 
              rows="4" 
              placeholder="What challenges are you trying to solve?" 
              value={formData.pain_points} 
              onChange={handleChange}
              aria-required="true"
            ></textarea>
          </div>
          
          <button type="submit" id="onboarding-submit-btn" className="btn" style={{ width: '100%', marginTop: '1rem' }} disabled={loading} aria-busy={loading}>
            {loading ? 'Initializing Aura...' : 'Start Conversation'}
          </button>
        </form>
      </div>
    </div>
  );
}

Onboarding.propTypes = {
  onComplete: PropTypes.func.isRequired,
};

export default Onboarding;
