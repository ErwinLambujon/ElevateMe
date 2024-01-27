from django.db import models

from django.contrib.auth.models import User

class VennDiagram(models.Model):
    field1 = models.TextField()
    field2 = models.TextField()
    field3 = models.TextField()
    filter = models.TextField(null=True)
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.field1} | {self.field2} | {self.field3} | {self.user_fk}"

class TwoVennDiagram(VennDiagram):
    pass
    def __str__(self):
        return f"{self.field1} | {self.field2}"

class ThreeVennDiagram(VennDiagram):
    def __str__(self):
        return f"{self.field1} | {self.field2} | {self.field3}"

class ProblemStatement(models.Model):
    statement = models.TextField()
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        abstract = True

    def to_dict(self):
        return {
            'id': self.id,
            'statement': self.statement,
            'user_fk': self.user_fk.username  # Assuming you want the username, change it accordingly
        }
class TwoProblemStatement(ProblemStatement):
    venn_fk = models.ForeignKey(TwoVennDiagram, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.to_dict())

class ThreeProblemStatement(ProblemStatement):
    venn_fk = models.ForeignKey(ThreeVennDiagram, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.to_dict())

