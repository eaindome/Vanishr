frontend/
├── public/                 # static assets
│   └── logo.svg
├── src/
│   ├── assets/             # images, global styles
│   │   └── tailwind.css
│   ├── components/         # reusable components
│   │   ├── Navbar.vue
│   │   ├── Sidebar.vue
│   │   ├── DataTable.vue
│   │   └── ProgressCard.vue
│   ├── layouts/            # layouts for pages
│   │   ├── AuthLayout.vue
│   │   └── DashboardLayout.vue
│   ├── pages/              # page views
│   │   ├── Login.vue
│   │   ├── Signup.vue
│   │   ├── Dashboard.vue
│   │   ├── DataBrokers.vue
│   │   ├── Requests.vue
│   │   └── Settings.vue
│   ├── router/             # vue-router setup
│   │   └── index.ts
│   ├── store/              # pinia (state management)
│   │   └── user.ts
│   ├── services/           # API calls
│   │   ├── api.ts
│   │   └── brokers.ts
│   ├── utils/              # helpers
│   │   └── formatDate.ts
│   ├── App.vue             # root component
│   └── main.ts             # entry point
├── index.html
├── package.json
├── tailwind.config.js
├── vite.config.ts
└── tsconfig.json
