import { ReactNode } from 'react'
import { Box, Container, AppBar, Toolbar, Typography, Button } from '@mui/material'
import { useNavigate } from 'react-router-dom'

interface LayoutProps {
  children: ReactNode
}

export function Layout({ children }: LayoutProps) {
  const navigate = useNavigate()

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            OpenMCP Workspace
          </Typography>
          <Button color="inherit" onClick={() => navigate('/')}>
            Commit Context
          </Button>
          <Button color="inherit" onClick={() => navigate('/history')}>
            History
          </Button>
        </Toolbar>
      </AppBar>
      <Container component="main" sx={{ flex: 1, py: 4 }}>
        {children}
      </Container>
      <Box component="footer" sx={{ py: 3, bgcolor: 'background.paper' }}>
        <Container maxWidth="lg">
          <Typography variant="body2" color="text.secondary" align="center">
            OpenMCP Workspace © {new Date().getFullYear()}
          </Typography>
        </Container>
      </Box>
    </Box>
  )
} 