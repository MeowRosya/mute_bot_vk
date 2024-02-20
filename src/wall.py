from config import service_api
from vkbottle_types.objects import WallWallpost
from VkAttachments import VkAttachments


async def get_wall_posts(domain: str, group_id: int) -> list[WallWallpost]:
    posts = []
    offset = 0

    while True:
        response, count, res = await service_api.wall.get(
            group_id=group_id, domain=domain, offset=offset, count=100
        )

        if len(res[1]) == 0:
            break

        posts += res[1]
        offset += 100

    return posts


def handle_main_group_posts(posts: list[WallWallpost]) -> VkAttachments:
    attachments = VkAttachments()

    for post in posts:
        if not post.attachments:
            continue
        buffer_audio = []
        text = post.text.lower() if post.text else ""
        attachments_with_audios = list(filter(lambda x: x.audio, post.attachments))
        attachments_with_photos = list(filter(lambda x: x.photo, post.attachments))

        for audio_attach in attachments_with_audios:
            attachment = f"audio{audio_attach.audio.owner_id}_{audio_attach.audio.id}"  # type: ignore
            buffer_audio.append(attachment)
            attachments.audios.append(attachment)

        if len(buffer_audio) > 1:
            attachments.mix.append(",".join(buffer_audio))

        for photo_attach in attachments_with_photos:
            attachment = f"photo{photo_attach.photo.owner_id}_{photo_attach.photo.id}"  # type: ignore

            if "quote" in text:
                attachments.quotes.append(attachment)
            elif "joke" in text:
                attachments.jokes.append(attachment)
            else:
                attachments.photos.append(attachment)

    return attachments


def handle_hent_group_posts(
    posts: list[WallWallpost], border_time: int = 0
) -> VkAttachments:
    attachments = VkAttachments()

    posts_with_attachments = list(
        filter(lambda x: x.attachments and x.date and (x.date >= border_time), posts)
    )

    for post in posts_with_attachments:
        text = post.text.lower() if post.text else ""

        attachments.horny_jokes += [
            f"photo{attachment.photo.owner_id}_{attachment.photo.id}"  # type: ignore
            for attachment in list(
                filter(lambda x: x.photo and "joke" in text, post.attachments)  # type: ignore
            )
        ]
        attachments.horny_photos += [
            f"photo{attachment.photo.owner_id}_{attachment.photo.id}"  # type: ignore
            for attachment in list(
                filter(lambda x: x.photo and "joke" not in text, post.attachments)  # type: ignore
            )
        ]

    return attachments


async def update_databases(domain: str):
    try:
        response, count, posts = await service_api.wall.get(domain=domain, count=3)
        return posts[1][:]
    except:
        return None
