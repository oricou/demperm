import { render, screen, fireEvent } from '@testing-library/react';
import { InfoCard } from './InfoCard';
import { describe, it, expect, vi } from 'vitest';

describe('InfoCard Component', () => {
  const mockItems = [
    { label: 'Name', value: 'John Doe' },
    { label: 'Email', value: 'john@example.com' },
    { label: 'Phone', value: '' },
  ];

  it('renders title and items in view mode', () => {
    render(<InfoCard title="User Details" items={mockItems} isEditing={false} />);
    
    expect(screen.getByText('User Details')).toBeInTheDocument();
    expect(screen.getByText('Name')).toBeInTheDocument();
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('Email')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
    // Empty value should render a dash
    expect(screen.getByText('—')).toBeInTheDocument();
  });

  it('renders inputs in edit mode', () => {
    render(<InfoCard title="User Details" items={mockItems} isEditing={true} />);
    
    const inputs = screen.getAllByRole('textbox');
    expect(inputs).toHaveLength(3);
    expect(inputs[0]).toHaveValue('John Doe');
    expect(inputs[1]).toHaveValue('john@example.com');
    expect(inputs[2]).toHaveValue('');
  });

  it('calls onChange when input is modified', () => {
    const handleChange = vi.fn();
    render(<InfoCard title="User Details" items={mockItems} isEditing={true} onChange={handleChange} />);
    
    const nameInput = screen.getAllByRole('textbox')[0];
    fireEvent.change(nameInput, { target: { value: 'Jane Doe' } });
    
    expect(handleChange).toHaveBeenCalledWith('Name', 'Jane Doe');
  });
});
