# Smart Review System - Setup & Migration Guide

## Quick Start

### Step 1: Database Migration

Run these commands in your terminal:

```bash
# Navigate to your project directory
cd c:\Users\Dell\OneDrive\Desktop\Project\Ecommerce Fake Products Reviews

# Create migrations for the new fields
python manage.py makemigrations Ecom_App

# Apply migrations to database
python manage.py migrate Ecom_App
```

**Expected Output:**
```
Operations to perform:
  Apply all migrations: Ecom_App
Running migrations:
  Applying Ecom_App.XXXX_auto_[date]... OK
```

### Step 2: Verify the Changes

```bash
# Open Django shell
python manage.py shell

# Test the new fields
from Ecom_App.models import Comments, Product

# Get a product
product = Product.objects.first()

# Check comments structure
comments = Comments.objects.filter(pid=product)
for comment in comments:
    print(f"ID: {comment.id}")
    print(f"Review Type: {comment.review_type}")
    print(f"Created At: {comment.created_at}")
    print(f"Comment: {comment.comment[:50]}...")
    print("---")

# Exit shell
exit()
```

---

## If You Have Existing Reviews

### Update Old Reviews

Old reviews won't have review_type set. Here's how to populate them:

**Option 1: Via Django Shell (Recommended)**

```bash
python manage.py shell
```

```python
from Ecom_App.models import Comments, Product
from django.db.models import Count

# For each user and product pair, mark the first review as Genuine; further reviews from the same user are flagged as Fake
for product in Product.objects.all():
    comments = Comments.objects.filter(pid=product).order_by('id')
    
    if comments.exists():
        # First review by this user = Genuine
        first_comment = comments.first()
        first_comment.review_type = 'Genuine'
        first_comment.save()
        
        # Rest = Fake
        remaining = comments.exclude(id=first_comment.id)
        remaining.update(review_type='Fake')
        
        print(f"✓ Product {product.id}: {comments.count()} reviews updated")

print("✓ All reviews updated!")

# Verify
genuine = Comments.objects.filter(review_type='Genuine').count()
fake = Comments.objects.filter(review_type='Fake').count()
print(f"\nStatistics:")
print(f"  Genuine: {genuine}")
print(f"  Fake: {fake}")

exit()
```

**Option 2: Direct SQL (for SQLite)**

```sql
-- Open db.sqlite3 with your favorite SQL client or:
-- python manage.py dbshell

-- Mark first review of each product as Genuine
UPDATE Comments SET review_type = 'Genuine' 
WHERE id IN (
    SELECT id FROM Comments c1 
    WHERE id = (SELECT id FROM Comments c2 WHERE c2.pid = c1.pid ORDER BY c2.id LIMIT 1)
);

-- Mark all others as Fake
UPDATE Comments SET review_type = 'Fake' 
WHERE review_type IS NULL OR review_type = '';
```

---

## Testing the System

### Test Scenario 1: Create a New Review

```bash
# 1. Start Django server
python manage.py runserver

# 2. Go to http://localhost:8000/Add_Review/1
#    (Replace 1 with a product ID)

# 3. Submit a review

# 4. Check database
python manage.py shell
```

```python
from Ecom_App.models import Comments, Product

product = Product.objects.get(id=1)
first_review = Comments.objects.filter(pid=product).first()

print(f"Review Type: {first_review.review_type}")
print(f"Expected: Genuine")
print(f"Created At: {first_review.created_at}")

exit()
```

### Test Scenario 2: Add Multiple Reviews

```bash
# 1. Create another user account
# 2. Log in with new account
# 3. Go to same product and submit another review
# 4. Check that it's marked as "Fake"
```

```python
python manage.py shell

from Ecom_App.models import Comments, Product

product = Product.objects.get(id=1)
reviews = Comments.objects.filter(pid=product).order_by('created_at')

for review in reviews:
    print(f"{review.uid.Name}: {review.review_type}")

# Expected output:
# User1: Genuine   (first review)
# User2: Fake      (second review)
# User3: Fake      (third review)

exit()
```

---

## Viewing the Results

### In Web Interface

1. Navigate to a product page (Add_Review)
2. Look for colored badges next to review author names:
   - **GREEN badge** = "✓ Genuine" (first review)
   - **RED badge** = "⚠ Fake" (subsequent reviews)

### In Database

```python
python manage.py shell

from Ecom_App.models import Comments

# View all reviews with their type
all_reviews = Comments.objects.all().values('id', 'uid__Name', 'pid__Product_Name', 'review_type')

for review in all_reviews:
    print(f"Product: {review['pid__Product_Name']}")
    print(f"  User: {review['uid__Name']}")
    print(f"  Type: {review['review_type']}")
    print()

exit()
```

### In Django Admin

```bash
# 1. Create superuser if you haven't
python manage.py createsuperuser

# 2. Start server
python manage.py runserver

# 3. Go to http://localhost:8000/admin/

# 4. Look for Comments section
# 5. Filter by review_type to see Genuine vs Fake reviews
```

---

## Common Commands Reference

### Django Shell Queries

```bash
python manage.py shell
```

```python
from Ecom_App.models import Comments, Product
from django.db.models import Count, Q

# 1. Count total reviews by type
print("Review Statistics:")
genuine = Comments.objects.filter(review_type='Genuine').count()
fake = Comments.objects.filter(review_type='Fake').count()
print(f"  Genuine: {genuine}")
print(f"  Fake: {fake}")

# 2. Find products with no genuine reviews
no_genuine = Product.objects.exclude(
    comments__review_type='Genuine'
)
print(f"\nProducts with no genuine reviews: {no_genuine.count()}")

# 3. Get fake reviews for a product
product_id = 1
fake_reviews = Comments.objects.filter(
    pid_id=product_id,
    review_type='Fake'
)
print(f"\nFake reviews for product {product_id}: {fake_reviews.count()}")

# 4. Most recent reviews
recent = Comments.objects.all().order_by('-created_at')[:5]
print("\nMost recent reviews:")
for review in recent:
    print(f"  - {review.uid.Name} ({review.review_type}) - {review.created_at}")

exit()
```

---

## Migration Troubleshooting

### Issue: "No changes detected in app 'Ecom_App'"

**Solution:** The migration may have already been created. Just run:

```bash
python manage.py migrate Ecom_App
```

### Issue: "django.db.utils.OperationalError: no such column"

**Solution:** 

```bash
# The migration wasn't applied to database
python manage.py migrate Ecom_App
```

### Issue: Can't create migration

**Solution:** 

```bash
# Check if there are unapplied migrations
python manage.py showmigrations

# Apply all migrations
python manage.py migrate

# Try again
python manage.py makemigrations Ecom_App
```

---

## Verifying Installation

### Checklist

- [ ] Models.py has new fields (review_type, created_at)
- [ ] Migration file created in migrations/
- [ ] Database migration applied (python manage.py migrate)
- [ ] Add_Review.html template updated with badges
- [ ] Views.py Add_Comment function updated
- [ ] Existing reviews properly populated with review_type
- [ ] New reviews show correct badges
- [ ] Database query returns correct values

---

## Backup Your Database Before Migration

### SQLite Backup

```bash
# Copy your database file
copy db.sqlite3 db.sqlite3.backup

# If something goes wrong, restore:
# del db.sqlite3
# rename db.sqlite3.backup db.sqlite3
# python manage.py migrate
```

### Alternative: Export Data Before Migration

```bash
# Export all data
python manage.py dumpdata Ecom_App > backup.json

# If needed, restore:
# python manage.py migrate zero Ecom_App  (careful!)
# python manage.py migrate Ecom_App
# python manage.py loaddata backup.json
```

---

## Performance Optimization (Optional)

### Add Database Indexes

If you have many reviews, add indexes for better performance:

```python
# In models.py, update Comments class Meta:

class Meta:
    db_table = "Comments"
    indexes = [
        models.Index(fields=['pid', 'review_type']),
        models.Index(fields=['created_at']),
        models.Index(fields=['uid']),
    ]
```

Then migrate:

```bash
python manage.py makemigrations Ecom_App
python manage.py migrate Ecom_App
```

---

## Monitor Database Changes

### View Database Schema

```bash
python manage.py shell
```

```python
from django.db import connection
from django.db.models import get_models

# Get Comments table info
from Ecom_App.models import Comments
print(Comments._meta.fields)

# Print each field
for field in Comments._meta.fields:
    print(f"{field.name}: {field.get_internal_type()}")

exit()
```

---

## Reset Everything (Nuclear Option - Use with Caution!)

If something goes wrong and you want to start fresh:

```bash
# WARNING: This deletes all reviews!

# 1. Delete old migration files (except initial)
# 2. Delete database
del db.sqlite3

# 3. Create new migration
python manage.py makemigrations Ecom_App

# 4. Create new database
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser
```

---

## Deployment Checklist

- [ ] Test locally first
- [ ] Backup database
- [ ] Run migrations on staging
- [ ] Test review functionality on staging
- [ ] Deploy to production
- [ ] Run migrations in production: `python manage.py migrate`
- [ ] Update existing review data with script above
- [ ] Test on live site
- [ ] Monitor for issues

---

## Next Steps

1. **Run migrations** (see Step 1 above)
2. **Update existing reviews** (see section above)
3. **Test the system** (see Testing section)
4. **Monitor** via Django shell or admin panel

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all files were updated correctly
3. Ensure migrations are applied: `python manage.py showmigrations`
4. Check Django console for error messages
5. Review SMART_REVIEW_SYSTEM_GUIDE.md for more details

---

**Last Updated**: March 5, 2026  
**Status**: Ready for Implementation ✅

