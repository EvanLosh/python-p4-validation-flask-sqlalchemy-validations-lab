from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, value):
        if len(value) == 0:
            raise ValueError('Names must have at least one character.')
        elif value in [author.name for author in Author.query.all()]:
            raise ValueError('Error: there is already an author with that name.')
        return value
    
    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if not len(number) == 10:
            raise ValueError('Phone numbers must have 10 digits.')
        for n in number:
            if int(n) not in [1,2,3,4,5,6,7,8,9,0]:
                raise ValueError('Phone numbers must be numbers.')
        return number
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self, key, title):
        if len(title) == 0:
            raise ValueError('Posts must have titles.')
        if ("Won't Believe" not in title) and ("Secret" not in title) and ("Top" not in title) and ("Guess" not in title):
            raise ValueError('Title does not contain clickbait keywords.')
        return title
    
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Posts must be at least 250 characters.')
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Summaries must not exceed 250 characters.')
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category must be either Fiction or Non-Fiction.')
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
