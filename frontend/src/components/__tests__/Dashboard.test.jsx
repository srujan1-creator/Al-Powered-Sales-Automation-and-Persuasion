import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Dashboard from '../Dashboard';

describe('Dashboard Component', () => {
  it('renders the Dashboard with provided data', () => {
    const mockContext = {
      company_size: '50-100',
      industry: 'Software',
      pain_points: 'High churn',
    };
    const mockConversation = { lead_score: 85 };

    render(<Dashboard conversation={mockConversation} context={mockContext} />);
    
    // Check score
    expect(screen.getByText('85')).toBeDefined();
    
    // Check context info
    expect(screen.getByText('50-100')).toBeDefined();
    expect(screen.getByText('Software')).toBeDefined();
    expect(screen.getByText('High churn')).toBeDefined();
    
    // Check End Conversation button exists and has aria-label
    const endBtn = screen.getByRole('button', { name: /end conversation/i });
    expect(endBtn).toBeDefined();
  });

  it('renders default values when no data is provided', () => {
    render(<Dashboard />);
    
    expect(screen.getByText('0')).toBeDefined();
    
    const placeholders = screen.getAllByText('N/A');
    expect(placeholders.length).toBe(3); // size, industry, pain points
  });
});
