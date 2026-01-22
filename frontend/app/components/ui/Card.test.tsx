import { render, screen } from '@testing-library/react';
import { Card } from './Card';
import { describe, it, expect } from 'vitest';

describe('Card', () => {
  it('renders children correctly', () => {
    render(<Card>Card Content</Card>);
    expect(screen.getByText('Card Content')).toBeInTheDocument();
  });

  it('renders with a string title', () => {
    render(<Card title="My Title">Card Content</Card>);
    expect(screen.getByRole('heading', { name: /my title/i, level: 3 })).toBeInTheDocument();
  });

  it('renders with a ReactNode title', () => {
    render(<Card title={<span>Custom Title</span>}>Card Content</Card>);
    expect(screen.getByText('Custom Title')).toBeInTheDocument();
    expect(screen.getByRole('heading', { level: 3 })).toBeInTheDocument();
  });

  it('applies custom className', () => {
    render(<Card className="my-custom-class">Content</Card>);
    expect(screen.getByText('Content').parentElement).toHaveClass('my-custom-class');
  });

  it('applies custom style', () => {
    render(<Card style={{ color: 'red' }}>Content</Card>);
    expect(screen.getByText('Content').parentElement).toHaveStyle({ color: 'red' });
  });

  it('applies variant styles', () => {
    const { rerender } = render(<Card variant="primary">Primary</Card>);
    expect(screen.getByText('Primary').parentElement).toHaveClass('bg-primary/10');

    rerender(<Card variant="secondary">Secondary</Card>);
    expect(screen.getByText('Secondary').parentElement).toHaveClass('bg-secondary/10');
  });

  it('uses default variant when none is provided', () => {
    render(<Card>Default</Card>);
    expect(screen.getByText('Default').parentElement).toHaveClass('bg-base-100');
  });
});
