from rest_framework import serializers

from candidates.models import Candidate

"""
Note: We may be able to replace all or nearly all of the
below CandidateSerializer with this ModelSerializer (given 
the addition of the necessary validators). Given the suggested
time limit, I did not get a chance to fully test whether 
the two would be equivalent. My guess is that it may not be
worth it due to the custom logic required for the update method.

class CandidateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ('id', 'name', 'years_exp',
                  'status', 'date_applied', 'reviewed',
                  'description', 'created', 'updated')
        read_only_fields = ('id',)
"""    
    
class CandidateSerializer(serializers.Serializer): 
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(max_length = 256)
    years_exp = serializers.IntegerField()
    status = serializers.ChoiceField(choices = Candidate.STATUS_CHOICES, default = Candidate.PENDING)
    date_applied = serializers.DateTimeField()
    reviewed = serializers.BooleanField(default = False)
    description = serializers.CharField()
    
    # These fields marked as read_only given that the related
    # fields in the model are auto_now/auto_now_add
    created = serializers.DateTimeField(read_only = True)
    updated = serializers.DateTimeField(read_only = True)
    
    def create(self, validated_data):
        return Candidate.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.years_exp = validated_data.get('years_exp', instance.years_exp)
        
        # Note -- unsure if the logic to auto-update candidate.reviewed
        # should be the sole method of updating the field, or if 
        # the option to force an update via PUT should be left in.
        # I've currently made the auto-update mandatory.
        updated_status = validated_data.get('status', instance.status)
        if instance.status == Candidate.PENDING:
            if updated_status == Candidate.REJECTED or updated_status == Candidate.ACCEPTED:
                instance.reviewed = True
        instance.status = updated_status
        
        instance.date_applied = validated_data.get('date_applied', instance.date_applied)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    
    def validate_years_exp(self, value):
        """
        Ensure that years_exp is not higher than 50.
        """
        if value > 50:
            raise serializers.ValidationError("Candidate's years of experience is higher than 50.")
        
        return value
        
    def validate_status(self, value):
        """
        Accepted candidates cannot be updated to rejected, and vice versa.
        """
        if not self.instance:
            return value
        if self.instance.status == Candidate.ACCEPTED:
            if value == Candidate.REJECTED:
                raise serializers.ValidationError("Candidate status cannot be updated from accepted to rejected.")
        if self.instance.status == Candidate.REJECTED:
            if value == Candidate.ACCEPTED:
                raise serializers.ValidationError("Candidate status cannot be changed from rejected to accepted.")
        
        return value