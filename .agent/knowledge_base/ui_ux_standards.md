# 🎨 UI/UX Standards (Pro Max)

## 🌈 Brand Palette
```typescript
colors: {
  primary: {
    DEFAULT: '#0048c4', // Update with brand primary
    dark: '#003399',
    light: '#3366ff',
  },
  accent: '#FFD700',
  success: '#10B981',
  error: '#EF4444',
  gray: {
    bg: '#f8fafc',
    border: '#e2e8f0',
  }
}
```

## 🔡 Typography (Inter/Sans)
- **H1 (Page Title)**: `text-3xl font-extrabold tracking-tight`
- **H2 (Section)**: `text-2xl font-bold`
- **H3 (Subtitle)**: `text-xl font-semibold`
- **Body**: `text-base leading-relaxed`
- **Small/Caption**: `text-sm text-gray-500`

## 📏 Spacing & Layout
- **Page Container**: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`
- **Section Spacing**: `py-12 md:py-20`
- **Grid Gap**: `gap-6 md:gap-8`

## 🧱 Core Components (Atomic)

### Cards
- **Style**: `bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden`
- **Hover**: `hover:shadow-xl hover:-translate-y-1 transition-all duration-300`

### Buttons
- **Primary**: `bg-primary text-white px-6 py-3 rounded-xl font-bold hover:brightness-110 active:scale-95 transition-all`
- **Ghost**: `bg-transparent border border-gray-200 text-gray-700 hover:bg-gray-50 rounded-xl transition-colors`

### Inputs
- **Style**: `w-full px-4 py-3 bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-primary/20 focus:border-primary rounded-xl transition-all`

## ✨ Micro-animations
- Sử dụng `framer-motion` cho các chuyển cảnh.
- Staggered children transitions (0.1s delay).
- Hover scale effect: `whileHover={{ scale: 1.02 }}`.

## ✅ UI/UX Checklist
- [ ] Tailwind class-first (No inline CSS).
- [ ] Mobile-first responsive grid.
- [ ] Accessible color contrast.
- [ ] Loading skeleton states cho async data.
- [ ] Smooth transitions cho mọi tương tác hover/click.
