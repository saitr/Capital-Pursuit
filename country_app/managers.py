from django.contrib.auth.base_user import BaseUserManager



class UserManager(BaseUserManager):
    use_in_migrations = True
    # method to create the user 
    def create_user(self,username,email,password=None,**extra_fields):

        if not username or not email:
            raise ValueError("Username, Email must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)   # to hash the password we do the set_password and then it hashes the password.
        user.save(using= self._db)
        return user
    # method to create the superuser 
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
