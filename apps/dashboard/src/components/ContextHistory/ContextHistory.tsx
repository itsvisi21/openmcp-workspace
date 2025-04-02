import { useState } from 'react'
import {
  Box,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  CircularProgress,
  Alert,
} from '@mui/material'
import { Delete as DeleteIcon, Visibility as ViewIcon } from '@mui/icons-material'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import { getContextHistory, deleteContext, ContextResponse } from '@services/api'

export function ContextHistory() {
  const [selectedContext, setSelectedContext] = useState<ContextResponse | null>(null)
  const queryClient = useQueryClient()

  const { data: contexts, isLoading, error } = useQuery('contexts', getContextHistory)

  const deleteMutation = useMutation((id: string) => deleteContext(id), {
    onSuccess: () => {
      queryClient.invalidateQueries('contexts')
    },
  })

  const handleDelete = (id: string) => {
    if (window.confirm('Are you sure you want to delete this context?')) {
      deleteMutation.mutate(id)
    }
  }

  const handleView = (context: ContextResponse) => {
    setSelectedContext(context)
  }

  const handleClose = () => {
    setSelectedContext(null)
  }

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    )
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        Failed to load context history. Please try again.
      </Alert>
    )
  }

  return (
    <>
      <Paper sx={{ p: 4 }}>
        <Typography variant="h5" gutterBottom>
          Context History
        </Typography>
        <List>
          {contexts?.map((context) => (
            <ListItem
              key={context.id}
              secondaryAction={
                <Box>
                  <IconButton edge="end" onClick={() => handleView(context)}>
                    <ViewIcon />
                  </IconButton>
                  <IconButton
                    edge="end"
                    onClick={() => handleDelete(context.id)}
                    disabled={deleteMutation.isLoading}
                  >
                    <DeleteIcon />
                  </IconButton>
                </Box>
              }
            >
              <ListItemText
                primary={context.type}
                secondary={new Date(context.created_at).toLocaleString()}
              />
            </ListItem>
          ))}
        </List>
      </Paper>

      <Dialog open={!!selectedContext} onClose={handleClose} maxWidth="md" fullWidth>
        <DialogTitle>Context Details</DialogTitle>
        <DialogContent>
          {selectedContext && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                Type: {selectedContext.type}
              </Typography>
              <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                Created: {new Date(selectedContext.created_at).toLocaleString()}
              </Typography>
              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Content
              </Typography>
              <Paper variant="outlined" sx={{ p: 2, bgcolor: 'background.default' }}>
                <Typography component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
                  {selectedContext.content}
                </Typography>
              </Paper>
              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Metadata
              </Typography>
              <Paper variant="outlined" sx={{ p: 2, bgcolor: 'background.default' }}>
                <Typography component="pre" sx={{ whiteSpace: 'pre-wrap' }}>
                  {JSON.stringify(selectedContext.metadata, null, 2)}
                </Typography>
              </Paper>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Close</Button>
        </DialogActions>
      </Dialog>
    </>
  )
} 