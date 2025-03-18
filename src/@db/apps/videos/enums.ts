export enum VideoStatus {
  DRAFT = 'draft',
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
}

export const VideoStatusMapping = {
  draft: { label: 'Draft', color: '#8884d8' },
  pending: { label: 'Pending', color: '#ff9800' },
  processing: { label: 'Processing', color: '#2196f3' },
  completed: { label: 'Completed', color: '#4caf50' },
  failed: { label: 'Failed', color: '#f44336' },
}
