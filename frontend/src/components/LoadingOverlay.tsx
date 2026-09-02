interface Props {
  message: string
}

export default function LoadingOverlay({ message }: Props) {
  return (
    <div className="loading-overlay" role="status" aria-live="polite">
      <div className="loading-overlay-card">
        <span className="spinner" />
        <p>{message}</p>
      </div>
    </div>
  )
}
