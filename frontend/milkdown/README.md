# Milkdown Editor for MarkRender

This is the Milkdown editor component for MarkRender, a powerful file conversion tool.

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run start
```

## Build and Deployment

```bash
# Build for production
npm run build

# Deploy to MarkRender plugin directory
npm run deploy

# Build and deploy in one command
npm run build-and-deploy
```

The build process will generate optimized files in the `dist` directory and automatically deploy them to the MarkRender plugin directory at `app/editor/plugins/milkdown`.

## Project Structure

- `src/` - Source code
- `src/main.ts` - Entry point
- `src/components/` - Vue components
- `vite.config.js` - Vite configuration
- `scripts/deploy.js` - Deployment script

## Key Features

- Rich Markdown editing with Milkdown Crepe
- Toolbar support for common formatting options
- Table, code block, and emoji support
- Integration with MarkRender's WebChannel communication system

## Troubleshooting

### Context "nodes" not found error

If you encounter the error "MilkdownError: Context 'nodes' not found, do you forget to inject it?", it's likely because required plugins are missing or not properly configured. Make sure you have included the necessary presets:

```typescript
import { commonmark } from '@milkdown/preset-commonmark';
import { gfm } from '@milkdown/preset-gfm';

// In your Crepe configuration:
new Crepe({
  // ... other config
  plugins: [
    commonmark,  // Required preset
    gfm,         // GitHub Flavored Markdown preset
    // ... other plugins
  ]
})
```

### Other common issues

1. **Large bundle size**: The vendor.js file is quite large due to all the dependencies. This is normal for a rich text editor like Milkdown.

2. **Build warnings**: You may see warnings about chunk sizes. These can be ignored for now, but for production you might want to consider code splitting.

3. **Runtime errors**: If you see other runtime errors, make sure all required dependencies are installed:
   ```bash
   npm install @milkdown/crepe @milkdown/plugin-history @milkdown/plugin-clipboard @milkdown/plugin-indent @milkdown/plugin-cursor @milkdown/preset-commonmark @milkdown/preset-gfm
   ```

### Error Analysis

The "Context 'nodes' not found" error typically occurs when:

1. Required presets (commonmark, gfm) are not included
2. Plugin order is incorrect
3. DOM element is not ready when the editor is initialized
4. Version mismatch between Crepe and plugins

Our solution includes:
- Proper import of required presets
- DOM ready check before initialization
- Error handling with fallback options
- Consistent versioning of all Milkdown packages

### Best Practices

1. Always ensure the DOM element exists before initializing the editor
2. Use proper error handling to catch initialization failures
3. Keep all Milkdown packages at the same version
4. Test the build in the actual MarkRender environment