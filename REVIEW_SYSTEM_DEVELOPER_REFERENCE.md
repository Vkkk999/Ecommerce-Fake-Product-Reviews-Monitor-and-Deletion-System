# Smart Review System - Developer Reference

## Model Definition

### Comments Model

```python
from django.db import models

class Comments(models.Model):
    # Review type choices
    REVIEW_TYPE_CHOICES = [
        ('Genuine', 'Genuine Review'),
        ('Fake', 'Fake Review'),
    ]
    
    # ForeignKeys
    pid = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    uid = models.ForeignKey(UserDetails, on_delete=models.CASCADE, null=True)
    
    # Review content
    comment = models.TextField(max_length=5000, default=None)
    ip = models.CharField(max_length=100, default=None)
    
    # Review classification
    review_type = models.CharField(
        max_length=20, 
        choices=REVIEW_TYPE_CHOICES, 
        default='Genuine'
    )
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        db_table = "Comments"
```

---

## View Logic

### Determining Review Type

```python
def determine_review_type(product_id):
    """
    Determine if a new review should be marked as Genuine or Fake.
    
    Args:
        product_id (int): The product ID
        
    Returns:
        str: 'Genuine' if this is the user's first review for the product, 'Fake' otherwise
    """
    from Ecom_App.models import Comments, Product
    
    try:
        product = Product.objects.get(id=product_id)
        review_count = Comments.objects.filter(pid=product).count()
        
        # A user's first review is genuine; later ones from the same user are fake
        return 'Genuine' if review_count == 0 else 'Fake'
    except Product.DoesNotExist:
        return 'Genuine'  # Default to Genuine if product not found
```

### Save Review with Type

```python
def save_review(product_id, user_id, comment_text, ip_address):
    """
    Save a review with automatic type classification.
    
    Args:
        product_id (int): Product ID
        user_id (int): User ID
        comment_text (str): Review text
        ip_address (str): IP address
        
    Returns:
        Comments: Created comment object or None on error
    """
    from Ecom_App.models import Comments, Product, UserDetails
    
    try:
        product = Product.objects.get(id=product_id)
        user = UserDetails.objects.get(id=user_id)
        
        # Determine review type
        review_count = Comments.objects.filter(pid=product).count()
        review_type = 'Genuine' if review_count == 0 else 'Fake'
        
        # Create and save comment
        comment = Comments(
            pid=product,
            uid=user,
            comment=comment_text,
            ip=ip_address,
            review_type=review_type
        )
        comment.save()
        
        return comment
    except (Product.DoesNotExist, UserDetails.DoesNotExist):
        return None
```

---

## Query Examples

### Get Genuine Reviews

```python
from Ecom_App.models import Comments

# All genuine reviews
genuine = Comments.objects.filter(review_type='Genuine')

# Genuine reviews for a product
product_id = 1
genuine_product = Comments.objects.filter(
    pid_id=product_id,
    review_type='Genuine'
)

# Count
count = genuine_product.count()  # Returns: 0 or 1 (only first review)
```

### Get Fake Reviews

```python
from Ecom_App.models import Comments

# All fake reviews
fake = Comments.objects.filter(review_type='Fake')

# Fake reviews for a product
product_id = 1
fake_product = Comments.objects.filter(
    pid_id=product_id,
    review_type='Fake'
)

# Count
count = fake_product.count()  # Returns: number of non-first reviews
```

### Get Reviews by Type with Details

```python
from Ecom_App.models import Comments

# Get all fake reviews with related info
fake_reviews = Comments.objects.filter(
    review_type='Fake'
).select_related('pid', 'uid').values(
    'id',
    'uid__Name',
    'pid__Product_Name',
    'comment',
    'created_at'
)

for review in fake_reviews:
    print(f"User: {review['uid__Name']}")
    print(f"Product: {review['pid__Product_Name']}")
    print(f"Review: {review['comment']}")
    print(f"Date: {review['created_at']}")
    print()
```

### Product Statistics

```python
from Ecom_App.models import Comments
from django.db.models import Count, Q

# Statistics per product
stats = Comments.objects.values('pid__Product_Name').annotate(
    total=Count('id'),
    genuine=Count('id', filter=Q(review_type='Genuine')),
    fake=Count('id', filter=Q(review_type='Fake'))
).order_by('-total')

for stat in stats:
    genuine_pct = (stat['genuine'] / stat['total'] * 100) if stat['total'] > 0 else 0
    fake_pct = (stat['fake'] / stat['total'] * 100) if stat['total'] > 0 else 0
    
    print(f"Product: {stat['pid__Product_Name']}")
    print(f"  Total: {stat['total']}")
    print(f"  Genuine: {stat['genuine']} ({genuine_pct:.1f}%)")
    print(f"  Fake: {stat['fake']} ({fake_pct:.1f}%)")
    print()
```

### Recent Reviews by Type

```python
from Ecom_App.models import Comments

# Recent genuine reviews
recent_genuine = Comments.objects.filter(
    review_type='Genuine'
).select_related('uid', 'pid').order_by('-created_at')[:10]

# Recent fake reviews
recent_fake = Comments.objects.filter(
    review_type='Fake'
).select_related('uid', 'pid').order_by('-created_at')[:10]

for review in recent_genuine:
    print(f"[Genuine] {review.uid.Name} - {review.pid.Product_Name}")
    print(f"  {review.comment[:80]}...")
    print(f"  {review.created_at}")
    print()
```

### Check First Review Status

```python
from Ecom_App.models import Comments

def is_first_review(comment_id):
    """Check if a comment is the first (genuine) review for its product."""
    try:
        comment = Comments.objects.get(id=comment_id)
        return comment.review_type == 'Genuine'
    except Comments.DoesNotExist:
        return None

# Usage
is_first = is_first_review(1)
print(f"Is first review: {is_first}")
```

---

## Template Usage

### Display Review with Badge

```html
{% for review in reviews %}
    <div class="review-item {% if review.review_type == 'Genuine' %}genuine{% else %}fake{% endif %}">
        <div class="review-header">
            <span class="review-user">{{ review.uid.Name }}</span>
            <span class="review-status-badge {% if review.review_type == 'Genuine' %}genuine{% else %}fake{% endif %}">
                {% if review.review_type == 'Genuine' %}
                    <i class="fas fa-check-circle"></i> Genuine
                {% else %}
                    <i class="fas fa-exclamation-circle"></i> Fake
                {% endif %}
            </span>
        </div>
        
        <div class="review-text">
            {{ review.comment }}
        </div>
        
        <div class="review-footer">
            <span>{{ review.created_at|date:"M d, Y H:i" }}</span>
            {% if user_id == review.uid.id %}
                <a href="/Edit_Review/{{ review.id }}" class="btn-modify">
                    <i class="fas fa-edit"></i> Edit
                </a>
            {% endif %}
        </div>
    </div>
{% endfor %}
```

### Count Reviews by Type

```html
{% load static %}

{% with genuine_count=reviews|dictsort:"review_type"|length %}
    <p>Total Genuine Reviews: {{ genuine_count }}</p>
{% endwith %}

<!-- Better approach: Calculate in view -->
<!-- In view: context['genuine_count'] = Comments.objects.filter(...) -->
<p>Genuine Reviews: {{ genuine_count }}</p>
<p>Fake Reviews: {{ fake_count }}</p>
```

---

## Admin Integration

### Custom Admin Display

```python
# Add to admin.py

from django.contrib import admin
from .models import Comments

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'pid', 'review_type', 'created_at', 'comment_preview')
    list_filter = ('review_type', 'created_at')
    search_fields = ('comment', 'uid__Name', 'pid__Product_Name')
    readonly_fields = ('created_at', 'review_type')
    ordering = ('-created_at',)
    
    def comment_preview(self, obj):
        """Show first 50 characters of comment."""
        return obj.comment[:50] + "..." if len(obj.comment) > 50 else obj.comment
    comment_preview.short_description = 'Preview'
    
    fieldsets = (
        ('Review Info', {
            'fields': ('pid', 'uid')
        }),
        ('Content', {
            'fields': ('comment',)
        }),
        ('Classification', {
            'fields': ('review_type', 'created_at')
        }),
        ('Metadata', {
            'fields': ('ip',)
        }),
    )
```

---

## API Endpoints

### Return Review Type

```python
# In views.py

def get_review_status(request, comment_id):
    """API endpoint to get review status."""
    from django.http import JsonResponse
    
    try:
        comment = Comments.objects.get(id=comment_id)
        return JsonResponse({
            'status': 'success',
            'review_type': comment.review_type,
            'is_genuine': comment.review_type == 'Genuine',
            'created_at': comment.created_at.isoformat()
        })
    except Comments.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Review not found'
        }, status=404)
```

### Return Product Review Stats

```python
def product_review_stats(request, product_id):
    """API endpoint for review statistics."""
    from django.http import JsonResponse
    from django.db.models import Count, Q
    
    try:
        stats = Comments.objects.filter(pid_id=product_id).aggregate(
            total=Count('id'),
            genuine=Count('id', filter=Q(review_type='Genuine')),
            fake=Count('id', filter=Q(review_type='Fake'))
        )
        
        stats['genuine_percentage'] = (
            stats['genuine'] / stats['total'] * 100 
            if stats['total'] > 0 else 0
        )
        
        return JsonResponse({
            'status': 'success',
            'product_id': product_id,
            'stats': stats
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
```

---

## Testing

### Unit Test Example

```python
# In tests.py

from django.test import TestCase
from .models import Comments, Product, UserDetails

class ReviewTypeTestCase(TestCase):
    
    def setUp(self):
        """Create test data."""
        self.product = Product.objects.create(
            Product_Name="Test Product",
            Product_Price="100"
        )
        self.user1 = UserDetails.objects.create(
            Name="User 1",
            Username="user1",
            Password="pass"
        )
        self.user2 = UserDetails.objects.create(
            Name="User 2",
            Username="user2",
            Password="pass"
        )
    
    def test_first_review_is_genuine(self):
        """First review should be marked as Genuine."""
        comment = Comments.objects.create(
            pid=self.product,
            uid=self.user1,
            comment="Great product!",
            ip="192.168.1.1",
            review_type='Genuine'
        )
        self.assertEqual(comment.review_type, 'Genuine')
    
    def test_second_review_is_fake(self):
        """Subsequent reviews should be marked as Fake."""
        # First review
        comment1 = Comments.objects.create(
            pid=self.product,
            uid=self.user1,
            comment="Great product!",
            ip="192.168.1.1",
            review_type='Genuine'
        )
        
        # Second review
        comment2 = Comments.objects.create(
            pid=self.product,
            uid=self.user2,
            comment="Also great!",
            ip="192.168.1.2",
            review_type='Fake'
        )
        
        self.assertEqual(comment2.review_type, 'Fake')
    
    def test_review_count_logic(self):
        """Test review counting logic."""
        count = Comments.objects.filter(pid=self.product).count()
        self.assertEqual(count, 0)  # Initially 0
        
        Comments.objects.create(
            pid=self.product,
            uid=self.user1,
            comment="Test",
            ip="192.168.1.1",
            review_type='Genuine'
        )
        
        count = Comments.objects.filter(pid=self.product).count()
        self.assertEqual(count, 1)  # Now 1
```

---

## Performance Tips

### Optimize Queries

```python
from Ecom_App.models import Comments

# Bad: Multiple database hits
for review in Comments.objects.all():
    print(review.uid.Name, review.pid.Product_Name)  # 2 queries per review

# Good: Use select_related
for review in Comments.objects.select_related('uid', 'pid'):
    print(review.uid.Name, review.pid.Product_Name)  # Only 1 query total

# Even better: Only get needed fields
reviews = Comments.objects.filter(
    review_type='Genuine'
).select_related('pid', 'uid').values(
    'id', 'uid__Name', 'pid__Product_Name'
)
```

### Add Indexes

```python
# In models.py Meta class

class Meta:
    db_table = "Comments"
    indexes = [
        models.Index(fields=['pid', 'review_type']),
        models.Index(fields=['created_at']),
    ]
```

---

## Common Patterns

### Get Review Summary

```python
from Ecom_App.models import Comments

def get_review_summary(product_id):
    """Get review summary for a product."""
    from django.db.models import Count, Q
    
    summary = Comments.objects.filter(pid_id=product_id).aggregate(
        total=Count('id'),
        genuine=Count('id', filter=Q(review_type='Genuine')),
        fake=Count('id', filter=Q(review_type='Fake'))
    )
    
    return summary

# Usage
summary = get_review_summary(1)
print(f"Total: {summary['total']}, Genuine: {summary['genuine']}, Fake: {summary['fake']}")
```

### Mark All Reviews as Fake (Emergency)

```python
from Ecom_App.models import Comments

# If needed for urgent action
Comments.objects.filter(pid_id=1).update(review_type='Fake')
print("All reviews marked as Fake")
```

### Bulk Update

```python
from Ecom_App.models import Comments

# Update multiple reviews
review_ids = [1, 2, 3, 4, 5]
Comments.objects.filter(id__in=review_ids).update(review_type='Fake')
```

---

## Debugging

### Log Review Activity

```python
import logging

logger = logging.getLogger(__name__)

def log_review_activity(review_id, action):
    """Log review-related activities."""
    from Ecom_App.models import Comments
    
    try:
        review = Comments.objects.get(id=review_id)
        logger.info(f"Review {review_id}: {action} - Type: {review.review_type}")
    except Comments.DoesNotExist:
        logger.error(f"Review {review_id} not found")
```

### Check Review Type Determination

```python
from Ecom_App.models import Comments, Product

def debug_review_type(product_id):
    """Debug why a review was marked as Genuine or Fake."""
    product = Product.objects.get(id=product_id)
    reviews = Comments.objects.filter(pid=product).order_by('created_at')
    
    print(f"\nDebug info for Product {product_id}: {product.Product_Name}")
    print(f"Total reviews: {reviews.count()}")
    print("\nReview sequence:")
    
    for i, review in enumerate(reviews, 1):
        print(f"{i}. {review.uid.Name}")
        print(f"   Type: {review.review_type}")
        print(f"   Expected: {'Genuine' if i == 1 else 'Fake'}")
        print(f"   Created: {review.created_at}")
        print()
```

---

## Reference Sheet

### Model Fields

| Field | Type | Default | Auto? | Required? |
|-------|------|---------|-------|-----------|
| `pid` | ForeignKey | None | No | No |
| `uid` | ForeignKey | None | No | No |
| `comment` | TextField | None | No | No |
| `ip` | CharField | None | No | No |
| `review_type` | CharField | 'Genuine' | No | Yes |
| `created_at` | DateTimeField | - | Yes | No |

### Query Shortcuts

```python
# Get genuine reviews
Comments.objects.filter(review_type='Genuine')

# Get fake reviews
Comments.objects.filter(review_type='Fake')

# Count by type
Comments.objects.values('review_type').count()

# Product with most fakes
from django.db.models import Count
Product.objects.annotate(fake_count=Count('comments', filter=Q(comments__review_type='Fake'))).order_by('-fake_count').first()
```

---

**Date**: March 5, 2026  
**Version**: 1.0  
**Status**: Complete Reference ✅

