import { render, screen, fireEvent } from '@testing-library/react';
import { Tabs, TabsList, TabsTrigger } from './Tabs';
import { describe, it, expect, vi } from 'vitest';

describe('Tabs Component', () => {
  it('renders default value correctly', () => {
    render(
      <Tabs defaultValue="tab1">
        <TabsList>
          <TabsTrigger value="tab1">Tab 1</TabsTrigger>
          <TabsTrigger value="tab2">Tab 2</TabsTrigger>
        </TabsList>
      </Tabs>
    );

    const tab1 = screen.getByRole('button', { name: /tab 1/i });
    const tab2 = screen.getByRole('button', { name: /tab 2/i });

    expect(tab1).toHaveClass('bg-white');
    expect(tab2).not.toHaveClass('bg-white');
  });

  it('switches tabs on click (uncontrolled)', () => {
    render(
      <Tabs defaultValue="tab1">
        <TabsList>
          <TabsTrigger value="tab1">Tab 1</TabsTrigger>
          <TabsTrigger value="tab2">Tab 2</TabsTrigger>
        </TabsList>
      </Tabs>
    );

    const tab2 = screen.getByRole('button', { name: /tab 2/i });
    fireEvent.click(tab2);

    expect(tab2).toHaveClass('bg-white');
    expect(screen.getByRole('button', { name: /tab 1/i })).not.toHaveClass('bg-white');
  });

  it('works in controlled mode', () => {
    const handleValueChange = vi.fn();
    const { rerender } = render(
      <Tabs value="tab1" onValueChange={handleValueChange}>
        <TabsList>
          <TabsTrigger value="tab1">Tab 1</TabsTrigger>
          <TabsTrigger value="tab2">Tab 2</TabsTrigger>
        </TabsList>
      </Tabs>
    );

    const tab2 = screen.getByRole('button', { name: /tab 2/i });
    fireEvent.click(tab2);

    expect(handleValueChange).toHaveBeenCalledWith('tab2');
    // Since it's controlled, it shouldn't change visual state unless prop updates
    expect(tab2).not.toHaveClass('bg-white');

    // Re-render with new value
    rerender(
      <Tabs value="tab2" onValueChange={handleValueChange}>
        <TabsList>
          <TabsTrigger value="tab1">Tab 1</TabsTrigger>
          <TabsTrigger value="tab2">Tab 2</TabsTrigger>
        </TabsList>
      </Tabs>
    );
    expect(tab2).toHaveClass('bg-white');
  });
});
