import { useState } from 'react'
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  CircularProgress,
  Alert,
} from '@mui/material'
import { useMutation } from 'react-query'
import { commitContext } from '@services/api'

type ContextType = 'code' | 'documentation' | 'conversation' | 'other'

interface ContextData {
  content: string
  type: ContextType
  metadata: Record<string, unknown>
}

export function ContextCommit() {
  const [content, setContent] = useState('')
  const [type, setType] = useState<ContextType>('code')
  const [metadata, setMetadata] = useState('')

  const { mutate, isLoading, error } = useMutation(
    (data: ContextData) => commitContext(data),
    {
      onSuccess: () => {
        setContent('')
        setType('code')
        setMetadata('')
      },
    }
  )

  const handleSubmit = () => {
    try {
      const parsedMetadata = metadata ? JSON.parse(metadata) : {}
      mutate({ content, type, metadata: parsedMetadata })
    } catch (e) {
      console.error('Invalid metadata JSON:', e)
    }
  }

  return (
    <Paper sx={{ p: 4 }}>
      <Typography variant="h5" gutterBottom>
        Commit Context
      </Typography>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Failed to commit context. Please try again.
        </Alert>
      )}
      <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <FormControl>
          <InputLabel>Context Type</InputLabel>
          <Select
            value={type}
            label="Context Type"
            onChange={(e) => setType(e.target.value as ContextType)}
          >
            <MenuItem value="code">Code</MenuItem>
            <MenuItem value="documentation">Documentation</MenuItem>
            <MenuItem value="conversation">Conversation</MenuItem>
            <MenuItem value="other">Other</MenuItem>
          </Select>
        </FormControl>
        <TextField
          label="Content"
          multiline
          rows={8}
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
        <TextField
          label="Metadata (JSON)"
          multiline
          rows={4}
          value={metadata}
          onChange={(e) => setMetadata(e.target.value)}
          placeholder='{"key": "value"}'
        />
        <Button
          variant="contained"
          onClick={handleSubmit}
          disabled={!content || isLoading}
          startIcon={isLoading && <CircularProgress size={20} />}
        >
          Commit Context
        </Button>
      </Box>
    </Paper>
  )
} 