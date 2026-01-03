from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile, ContractorProfile


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user with a role
    ✅ NID Verification - Nepal format support during registration
    ✅ Contractor Qualification System - Auto-create contractor profile
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role', 'PUBLIC')
    nepal_nid = request.data.get('nepal_nid', '')  # ✅ NID Verification
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create user
    user = User.objects.create_user(
        username=username,
        email=email or '',
        password=password
    )
    
    # Create user profile with role and optional NID
    profile = UserProfile.objects.create(
        user=user, 
        role=role,
        nepal_nid=nepal_nid if nepal_nid else None
    )
    
    # ✅ Contractor Qualification System - Auto-create ContractorProfile for contractors
    contractor_profile_data = None
    if role == 'CONTRACTOR':
        contractor_profile = ContractorProfile.objects.create(user=user)
        contractor_profile_data = {
            'rating': str(contractor_profile.rating),
            'is_suspended': contractor_profile.is_suspended,
            'skill_level': contractor_profile.skill_level
        }
    
    # Generate tokens
    refresh = RefreshToken.for_user(user)
    
    response_data = {
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': role,
            'nepal_nid': nepal_nid if nepal_nid else None,
            'nid_verified': False
        },
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    }
    
    if contractor_profile_data:
        response_data['contractor_profile'] = contractor_profile_data
    
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Login user and return JWT tokens with role
    ✅ Suspension System - Check if contractor is suspended
    """
    from django.contrib.auth import authenticate
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'role': 'PUBLIC'}
    )
    
    # ✅ Suspension System - Check and include suspension status for contractors
    suspension_info = None
    if profile.role == 'CONTRACTOR':
        contractor_profile, _ = ContractorProfile.objects.get_or_create(user=user)
        if contractor_profile.is_suspended:
            suspension_info = {
                'is_suspended': True,
                'reason': contractor_profile.suspension_reason,
                'suspended_at': contractor_profile.suspended_at.isoformat() if contractor_profile.suspended_at else None
            }
    
    # Generate tokens
    refresh = RefreshToken.for_user(user)
    
    response_data = {
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': profile.role,
            'nepal_nid': profile.nepal_nid,
            'nid_verified': profile.nid_verified
        },
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    }
    
    if suspension_info:
        response_data['suspension'] = suspension_info
    
    return Response(response_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    Get current user profile with contractor details if applicable
    """
    user = request.user
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'role': 'PUBLIC'}
    )
    
    response_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': profile.role,
        'nepal_nid': profile.nepal_nid,
        'nid_verified': profile.nid_verified
    }
    
    # Include contractor profile data if user is a contractor
    if profile.role == 'CONTRACTOR':
        try:
            contractor_profile = ContractorProfile.objects.get(user=user)
            response_data['contractor_profile'] = {
                'rating': str(contractor_profile.rating),
                'is_suspended': contractor_profile.is_suspended,
                'suspension_reason': contractor_profile.suspension_reason if contractor_profile.is_suspended else None,
                'skill_level': contractor_profile.skill_level,
                'years_of_experience': contractor_profile.years_of_experience,
                'test_passed': contractor_profile.test_passed,
                'total_projects_completed': contractor_profile.total_projects_completed,
                'total_projects_failed': contractor_profile.total_projects_failed,
                'ai_rating': str(contractor_profile.ai_rating) if contractor_profile.ai_rating else None,
                'ai_risk_score': str(contractor_profile.ai_risk_score) if contractor_profile.ai_risk_score else None
            }
        except ContractorProfile.DoesNotExist:
            pass
    
    return Response(response_data)
