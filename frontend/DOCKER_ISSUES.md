# Frontend Docker Build Known Issue

## TypeScript Compatibility Issue

### Problem
The frontend Docker build currently fails due to TypeScript compatibility issues between:
- TypeScript version: ~4.5.5 (used in project)
- @types/lodash: Uses newer template literal syntax
- Node.js version: Newer versions in Docker

### Error
```
TS1005: '?' expected.
type StringToNumber<T> = T extends `${infer N extends number}` ? N : never;
```

### Temporary Solutions

#### Option 1: Use Pre-built Distribution
If the `dist` directory is available:

```dockerfile
FROM nginx:stable-alpine
COPY dist/ /usr/share/nginx/html/
COPY docker/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Option 2: Update Dependencies
Update `package.json`:

```bash
npm install typescript@~5.0.0
npm install @types/lodash@^4.14.195
npm audit fix
```

#### Option 3: Downgrade Node.js
Use Node.js 16 which has better compatibility:

```dockerfile
FROM node:16-alpine as build-stage
```

#### Option 4: Exclude Type Checking
Add to `vue.config.js`:

```javascript
module.exports = {
  chainWebpack: config => {
    config.plugin('fork-ts-checker').tap(args => {
      args[0].typescript.enabled = false
      return args
    })
  }
}
```

### Recommended Solution
For production deployment, the best approach is to:

1. Build locally or in CI/CD pipeline
2. Use the built `dist` directory in Docker
3. Serve with nginx

### Build Script Example
```bash
#!/bin/bash
# build-frontend.sh
cd frontend
npm install
npm run build
docker build -f Dockerfile.simple -t lab-website-frontend .
```

Where `Dockerfile.simple`:
```dockerfile
FROM nginx:stable-alpine
COPY dist/ /usr/share/nginx/html/
COPY docker/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

This approach separates the build process from containerization, which is often preferable in production environments.