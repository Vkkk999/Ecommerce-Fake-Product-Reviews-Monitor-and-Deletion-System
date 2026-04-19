# Product Card CSS - Quick Reference Guide

## Copy-Paste Ready CSS Snippets

### 1. Fixed Image Height with No Distortion

```css
.product-image-wrapper {
    position: relative;
    height: 280px;
    overflow: hidden;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.product-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
}
```

**Key Properties**:
- `object-fit: cover` - Scales image to fill container without distortion
- `object-position: center` - Centers the image within container

---

### 2. Smooth Hover Zoom Effect

```css
.product-image {
    transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.product-card:hover .product-image {
    transform: scale(1.08) rotate(2deg);
}
```

**Parameters**:
- `scale(1.08)` - 8% zoom on hover (change to 1.15 for 15% zoom)
- `rotate(2deg)` - 2 degree rotation (remove for no rotation)
- `0.5s` - Animation duration

---

### 3. Card Shadow & Depth

```css
.product-card {
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.product-card:hover {
    transform: translateY(-12px);
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
}
```

**Parameters**:
- `0 8px 32px` - Normal shadow (X offset, blur, spread)
- `-12px` - Lift distance on hover (make larger for more lift)
- Shadow color with alpha (0.15 = 15% opacity)

---

### 4. Rounded Image Corners  

```css
.product-image-wrapper {
    border-radius: 16px;
    overflow: hidden;
}

.product-card {
    border-radius: 16px;
    overflow: hidden;
}
```

**Radius Values**:
- `16px` - Smooth, modern rounded corners
- `8px` - Slightly rounded
- `24px` - Very rounded
- `50%` - Perfect circle (with square container)

---

### 5. Responsive Grid Layout

```css
.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
}

@media (max-width: 1023px) {
    .products-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 767px) {
    .products-grid {
        grid-template-columns: 1fr;
    }
}
```

**Parameters**:
- `300px` - Minimum card width (adjust to 250px or 350px)
- `2rem` - Gap between cards (adjust to 1rem or 3rem)
- Breakpoints: 1023px (tablet), 767px (mobile)

---

### 6. Glassmorphism Card Background

```css
.product-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 100%);
    backdrop-filter: blur(4px);
    border: 1px solid rgba(255, 255, 255, 0.3);
}
```

**For Colored Background**:
```css
/* Blue-tinted glass */
background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);

/* Dark glass */
background: linear-gradient(135deg, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0.7) 100%);
```

---

### 7. Product Image Perfect Square (Detail Page)

```css
.product-image-container {
    position: relative;
    width: 100%;
    padding-bottom: 100%;  /* 1:1 aspect ratio */
    overflow: hidden;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.product-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
}
```

**Aspect Ratio Values**:
- `100%` - 1:1 (Square) for detail page
- `66.67%` - 3:2 ratio
- `75%` - 4:3 ratio
- `56.25%` - 16:9 widescreen

---

### 8. Gradient Text (Price Display)

```css
.product-price {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
```

**Color Combinations**:
```css
/* Purple to Pink */
linear-gradient(135deg, #667eea 0%, #764ba2 100%)

/* Green to Blue */
linear-gradient(135deg, #11998e 0%, #38ef7d 100%)

/* Orange to Red */
linear-gradient(135deg, #f093fb 0%, #f5576c 100%)

/* Cyan to Blue */
linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)
```

---

### 9. Card Hover Lift Animation

```css
.product-card {
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.product-card:hover {
    transform: translateY(-12px);
}
```

**Cubic Bezier Functions**:
```css
/* Smooth, bouncy */
cubic-bezier(0.175, 0.885, 0.32, 1.275)

/* Smooth, standard */
cubic-bezier(0.645, 0.045, 0.355, 1)

/* Easy in-out */
cubic-bezier(0.4, 0, 0.2, 1)

/* Linear */
linear
```

---

### 10. Animated Badge

```css
.product-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    animation: pulse 2s infinite;
    z-index: 2;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
```

**Animation Variations**:

```css
/* Bounce effect */
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

/* Glow effect */
@keyframes glow {
    0%, 100% { box-shadow: 0 0 5px rgba(245, 87, 108, 0.5); }
    50% { box-shadow: 0 0 20px rgba(245, 87, 108, 0.8); }
}

/* Rotate effect */
@keyframes rotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
```

---

### 11. Empty State Message

```css
.empty-state {
    grid-column: 1 / -1;
    text-align: center;
    padding: 4rem 2rem;
}

.empty-state-icon {
    font-size: 4rem;
    color: #ccc;
    margin-bottom: 1rem;
}

.empty-state-text {
    color: #999;
    font-size: 1.1rem;
}
```

---

### 12. Page Header with Gradient

```css
.page-title {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}

.page-subtitle {
    color: #666;
    font-size: 1.1rem;
    font-weight: 500;
}
```

---

## Color Palette Reference

### Primary Colors
```
Purple:     #667eea
Dark Purple: #764ba2
Light Blue: #f5f7fa
```

### Accent Colors
```
Pink:       #f093fb
Red:        #f5576c
Cyan:       #4facfe
Teal:       #00f2fe
Green:      #11998e
Lime:       #38ef7d
```

### Text Colors
```
Dark:       #333333 (for headings)
Gray:       #666666 (for body text)
Light Gray: #999999 (for secondary text)
```

### Shadows
```
Light:   rgba(31, 38, 135, 0.15)   /* 15% opacity */
Medium:  rgba(102, 126, 234, 0.3)  /* 30% opacity */
Dark:    rgba(0, 0, 0, 0.2)        /* 20% opacity */
```

---

## Common CSS Values Quick Reference

### Font Sizes
```css
font-size: 2.5rem;  /* Large titles */
font-size: 1.8rem;  /* Section titles */
font-size: 1.2rem;  /* Card titles */
font-size: 1rem;    /* Normal text */
font-size: 0.9rem;  /* Small text */
font-size: 0.85rem; /* Extra small */
font-size: 0.8rem;  /* Badge text */
```

### Spacing (Padding/Margin)
```css
/* Using rem (1rem = 16px) */
4rem    /* 64px - Large spacing */
3rem    /* 48px - Medium spacing */
2rem    /* 32px - Standard spacing */
1.5rem  /* 24px - Compact spacing */
1rem    /* 16px - Base spacing */
0.5rem  /* 8px - Tight spacing */
```

### Transition Times
```css
0.3s cubic-bezier(0.645, 0.045, 0.355, 1)     /* Quick alerts */
0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)  /* Card hover */
0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)  /* Image zoom */
0.6s ease                                      /* Page animations */
```

### Border Radius
```css
50%     /* Perfect circle */
24px    /* Very rounded */
16px    /* Modern rounded (recommended) */
8px     /* Slightly rounded */
4px     /* Subtle rounding */
0       /* No rounding */
```

---

## Testing CSS Changes

### To Test Hover Effects on Mobile
```html
<!-- Add this class to test on mobile/tablet -->
.product-card:active {
    transform: translateY(-12px);
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
}
```

### To Disable Animations (Accessibility)
```css
@media (prefers-reduced-motion: reduce) {
    .product-card,
    .product-image {
        transition: none;
        animation: none;
    }
}
```

### Performance Check
```scss
/* ✅ GPU-accelerated (use these) */
transform: scale(), rotate(), translateY()
opacity: 0/1

/* ❌ CPU-intensive (avoid animating these) */
width, height, padding, margin
left, right, top, bottom
```

---

## Browser DevTools Tips

### Debug Image Display
```javascript
/* In Chrome DevTools Console */
// Check if object-fit is applied
document.querySelector('.product-image').getComputedStyle()

// Check image dimensions
const img = document.querySelector('.product-image');
console.log(`Image: ${img.naturalWidth}x${img.naturalHeight}`);
console.log(`Display: ${img.offsetWidth}x${img.offsetHeight}`);
```

### Performance Testing
```javascript
/* Measure animation performance */
performance.mark('card-hover-start');
// Hover on card
performance.mark('card-hover-end');
performance.measure('card-hover', 'card-hover-start', 'card-hover-end');
```

---

## Common Issues & Solutions

### Image Distorted
```scss
❌ WRONG:
img { width: 100%; height: 100%; }  /* May stretch */

✅ CORRECT:
img { 
    width: 100%; 
    height: 100%; 
    object-fit: cover;  /* KEY */
    object-position: center;
}
```

### Card Not Hovering Smoothly
```scss
❌ WRONG:
.card:hover { box-shadow: ...; }  /* No transition */

✅ CORRECT:
.card {
    transition: all 0.4s ease;
}
.card:hover { box-shadow: ...; }
```

### Not Responsive on Mobile
```scss
❌ WRONG:
.grid { grid-template-columns: repeat(4, 1fr); }  /* Fixed 4 columns */

✅ CORRECT:
.grid { 
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}
/* Or add mobile breakpoint */
@media (max-width: 767px) {
    .grid { grid-template-columns: 1fr; }
}
```

---

## Version Information

**Created**: March 5, 2026  
**CSS Framework**: Pure CSS3 (No preprocessor required)  
**Browser Support**: All modern browsers (Chrome, Firefox, Safari, Edge)  
**Mobile Support**: iOS Safari 10+, Chrome Mobile

---

**End of CSS Reference Guide**

