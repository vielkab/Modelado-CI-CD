# Landing con CI/CD (Integración y Despliegue Continuos)

Sitio estático que se **publica solo** cuando haces `git push` a `main`. Nadie sube archivos por FTP ni copia carpetas a mano.

## Cambiar texto o colores

1. Edita `index.html` (textos) o `css/styles.css` (variables en `:root`, p. ej. `--color-primary`).
2. En local, opcional: abre `index.html` en el navegador para previsualizar.
3. Commit y push:

```bash
git add .
git commit -m "Cambiar color primario y titular"
git push origin main
```

En unos minutos la URL de GitHub Pages mostrará los cambios.

## Puesta en marcha (una sola vez)

1. Crea un repositorio en GitHub y sube este proyecto:

```bash
git init
git add .
git commit -m "Landing con pipeline CI/CD"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

2. En el repo: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

3. Tras el primer workflow exitoso, la URL será algo como:  
   `https://TU_USUARIO.github.io/TU_REPO/`

## Estructura

```
.
├── index.html              # Contenido
├── css/styles.css          # Estilos (colores en :root)
├── .github/workflows/
│   └── deploy.yml          # Pipeline CI/CD
└── README.md
```

