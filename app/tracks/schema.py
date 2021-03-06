import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.db.models import Q

from .models import Track, Like
# from users.schema import UserType
from app.registration.schema import UserType


class TrackType(DjangoObjectType):
    class Meta:
        model = Track


class LikeType(DjangoObjectType):
    class Meta:
        model = Like


class Query(graphene.ObjectType):
    tracks = graphene.List(
                            TrackType,
                            search=graphene.String(),
                            first=graphene.Int(),
                            skip=graphene.Int(),
                        )
    likes = graphene.List(LikeType)

    def resolve_tracks(
                        self,
                        info,
                        search=None,
                        first=None,
                        skip=None,
                        **kwargs
                    ):
        qs = Track.objects.all()

        if search:
            filter = (
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(url__icontains=search) |
                Q(avarta__icontains=search) |
                Q(posted_by__username__icontains=search)

            )
            qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    def resolve_likes(self, info):
        return Like.objects.all()


class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()
        avarta = graphene.String()

    def mutate(self, info, title, description, url, avarta):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('You need to login to add a track!')

        track = Track(
            title=title,
            description=description,
            url=url,
            avarta=avarta,
            posted_by=user)
        track.save()
        return CreateTrack(track=track)


class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()
        avarta = graphene.String()

    def mutate(self, info, track_id, title, url, avarta, description):
        user = info.context.user
        track = Track.objects.get(id=track_id)

        if track.posted_by != user:
            raise GraphQLError('Not permitted to update this track.')

        track.title = title
        track.description = description
        track.url = url
        track.avarta = avarta

        track.save()

        return UpdateTrack(track=track)


class DeletTrack(graphene.Mutation):
    track_id = graphene.Int()

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user

        track = Track.objects.get(id=track_id)

        if track.posted_by != user:
            raise GraphQLError("Not permitted to delete this track.")

        track.delete()

        return DeletTrack(track_id=track_id)


class CreateLike(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Login to like tracks")

        track = Track.objects.get(id=track_id)

        if not track:
            raise GraphQLError("Cannot find track track with given id.")

        Like.objects.create(
            user=user,
            track=track
        )

        return CreateLike(user=user, track=track)


class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeletTrack.Field()
    create_like = CreateLike.Field()
