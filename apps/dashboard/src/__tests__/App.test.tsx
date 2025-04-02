import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import App from '../App';

// Mock the API service
vi.mock('@services/api', () => ({
  commitContext: async () => ({ success: true }),
}));

describe('App', () => {
  it('renders without crashing', () => {
    console.log('Starting render test...');
    
    try {
      render(<App />);
      console.log('Render successful');
    } catch (error) {
      console.error('Render failed:', error);
      throw error;
    }

    expect(document.body).toBeDefined();
    console.log('Test completed');
  });
}); 