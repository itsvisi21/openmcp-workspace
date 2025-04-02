# Agent Protocol Documentation

## Overview
This document outlines the protocol for AI agents interacting with the OpenMCP Workspace system. The protocol ensures consistent and reliable communication between agents and the system components.

## Agent Requirements
1. Must read project.status.json before any operation
2. Must update current_applied_action.log after each action
3. Must follow feature-driven development approach
4. Must maintain modular architecture principles
5. Must document all changes and decisions

## Communication Protocol

### Context Window Management
1. **Reading Context**
   - Read project.status.json
   - Read relevant feature documentation
   - Read current_applied_action.log
   - Read any relevant code files

2. **Updating Context**
   - Update project.status.json with new files/changes
   - Update current_applied_action.log with actions taken
   - Update backlog.json if feature status changes

### Feature Implementation
1. **Planning Phase**
   - Review feature requirements
   - Identify affected components
   - Plan implementation steps
   - Document approach

2. **Implementation Phase**
   - Follow modular design principles
   - Implement tests first
   - Make incremental changes
   - Document all changes

3. **Review Phase**
   - Verify feature completeness
   - Run test suite
   - Update documentation
   - Update status files

## File Management Protocol

### Creating Files
1. Create file with appropriate structure
2. Update project.status.json
3. Update current_applied_action.log
4. Document in relevant feature docs

### Modifying Files
1. Read existing content
2. Make targeted changes
3. Update project.status.json
4. Update current_applied_action.log

### Deleting Files
1. Verify no dependencies
2. Remove file
3. Update project.status.json
4. Update current_applied_action.log

## Error Handling
1. Document all errors
2. Implement graceful fallbacks
3. Maintain system state
4. Provide clear error messages

## Testing Protocol
1. Write unit tests
2. Write integration tests
3. Run test suite
4. Document test coverage

## Documentation Protocol
1. Update relevant docs
2. Add inline documentation
3. Update API documentation
4. Maintain changelog

## Security Protocol
1. Follow security best practices
2. Validate all inputs
3. Sanitize all outputs
4. Log security events

## Future Considerations
1. Web4 integration planning
2. Decentralization path
3. Smart contract integration
4. IPFS migration strategy 