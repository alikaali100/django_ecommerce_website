class TimestampMixin:
    def as_dict(self):
        return {
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
