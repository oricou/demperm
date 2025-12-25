import { render, screen } from '@testing-library/react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, StatValue } from './Card';
import { describe, it, expect } from 'vitest';

describe('Card Components', () => {
  it('renders Card with content', () => {
    render(<Card>Card Content</Card>);
    expect(screen.getByText('Card Content')).toBeInTheDocument();
  });

  it('renders CardHeader, Title, Description, and Content', () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>My Title</CardTitle>
          <CardDescription>My Description</CardDescription>
        </CardHeader>
        <CardContent>My Content</CardContent>
      </Card>
    );

    expect(screen.getByRole('heading', { name: /my title/i })).toBeInTheDocument();
    expect(screen.getByText('My Description')).toBeInTheDocument();
    expect(screen.getByText('My Content')).toBeInTheDocument();
  });

  it('renders StatValue correctly', () => {
    render(<StatValue label="Total Votes" value="123" />);
    expect(screen.getByText('Total Votes')).toBeInTheDocument();
    expect(screen.getByText('123')).toBeInTheDocument();
  });
});
