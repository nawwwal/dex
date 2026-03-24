# Common Animation Patterns

## Page Transition
```tsx
<AnimatePresence mode="wait">
  <motion.div key={pathname} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.2 }}>
    {children}
  </motion.div>
</AnimatePresence>
```

## Toast Notification
```tsx
<motion.div initial={{ x: 50, opacity: 0 }} animate={{ x: 0, opacity: 1 }} exit={{ x: 50, opacity: 0 }} transition={{ type: 'spring', stiffness: 400, damping: 30 }} />
```

## Staggered List
```tsx
const list = { visible: { transition: { staggerChildren: 0.07 } } };
const item = { hidden: { opacity: 0, x: -20 }, visible: { opacity: 1, x: 0 } };
```

## Number Counter
```tsx
<motion.span initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
  <motion.span>{animatedNumber}</motion.span>
</motion.span>
```

## Drawer (Bottom Sheet)
```tsx
initial={{ y: '100%' }} animate={{ y: 0 }} exit={{ y: '100%' }}
// Apple-style spring (recommended): easier to reason about
transition={{ type: 'spring', duration: 0.5, bounce: 0.2 }}
// Traditional physics alternative: { type: 'spring', stiffness: 300, damping: 30 }
```
