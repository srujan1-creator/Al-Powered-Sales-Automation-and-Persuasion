import PropTypes from 'prop-types';

function Dashboard({ conversation, context }) {
  const score = conversation?.lead_score || 0;
  
  // Calculate stroke dasharray for the score circle if needed, 
  // but we are using conic-gradient in CSS which is handled via --score CSS variable.
  const scoreStyle = { '--score': score };
  
  let scoreColor = 'var(--success)';
  if (score < 40) scoreColor = 'var(--danger)';
  else if (score < 70) scoreColor = 'var(--warning)';

  return (
    <div className="dashboard-card glass-panel animate-fade-in" role="complementary" aria-label="Dashboard">
      <h3>Lead Analysis</h3>
      
      <div className="score-container">
        <div 
          className="score-circle" 
          style={{ ...scoreStyle, background: `conic-gradient(${scoreColor} calc(var(--score) * 1%), rgba(255, 255, 255, 0.1) 0)` }}
          role="meter"
          aria-valuenow={Math.round(score)}
          aria-valuemin="0"
          aria-valuemax="100"
          aria-label="Conversion Probability Score"
        >
          <span>{Math.round(score)}</span>
        </div>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Conversion Probability</p>
      </div>
      
      <div className="context-details">
        <h4 style={{ marginBottom: '1rem', borderBottom: '1px solid var(--surface-border)', paddingBottom: '0.5rem' }}>
          Lead Context
        </h4>
        
        <div className="context-item">
          <div className="context-label">Company Size</div>
          <div className="context-value">{context?.company_size || 'N/A'}</div>
        </div>
        
        <div className="context-item">
          <div className="context-label">Industry</div>
          <div className="context-value">{context?.industry || 'N/A'}</div>
        </div>
        
        <div className="context-item">
          <div className="context-label">Key Challenge</div>
          <div className="context-value" style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            {context?.pain_points || 'N/A'}
          </div>
        </div>
      </div>
      
      <div style={{ marginTop: '2rem' }}>
        <button id="dashboard-end-btn" className="btn btn-secondary" style={{ width: '100%' }} onClick={() => window.location.reload()} aria-label="End Conversation">
          End Conversation
        </button>
      </div>
    </div>
  );
}

Dashboard.propTypes = {
  conversation: PropTypes.shape({
    lead_score: PropTypes.number,
  }),
  context: PropTypes.shape({
    company_size: PropTypes.string,
    industry: PropTypes.string,
    pain_points: PropTypes.string,
  }),
};

export default Dashboard;
