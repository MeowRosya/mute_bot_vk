import asyncio
from config import service_api
from vkbottle_types.objects import WallWallpostFull
from VkAttachments import VkAttachments


async def get_wall_posts(group_id: int) -> list[WallWallpostFull]:
    posts = []
    offset = 0

    while True:
        res = await service_api.wall.get(owner_id=group_id, offset=offset, count=100)
        recieved_posts = res.items
        if recieved_posts is None or len(recieved_posts) == 0:
            break

        posts += recieved_posts
        offset += 100

    return posts


def handle_post_attachments(post: WallWallpostFull) -> tuple[list[str], list[str]]:
    """Returns array of stringify attachments of photos and audios"""

    buffer_audio: list[str] = []
    buffer_photo: list[str] = []

    if post.attachments is None:
        return buffer_photo, buffer_audio

    for attachment in post.attachments:
        if attachment.audio:
            attachment = f"audio{attachment.audio.owner_id}_{attachment.audio.id}"
            buffer_audio.append(attachment)

        elif attachment.photo:
            attachment = f"photo{attachment.photo.owner_id}_{attachment.photo.id}"
            buffer_photo.append(attachment)

    return buffer_photo, buffer_audio


def handle_main_group_posts(posts: list[WallWallpostFull]) -> VkAttachments:
    attachments = VkAttachments()

    for post in posts:
        if not post.attachments:
            continue

        text = post.text.lower() if post.text else ""
        buffer_photos, buffer_audio = handle_post_attachments(post)

        attachments.audios += buffer_audio

        # group audio only if post has more than 1 audio attachment
        if len(buffer_audio) > 1:
            attachments.mix.append(",".join(buffer_audio))

        if "quote" in text:
            attachments.quotes += buffer_photos
        elif "joke" in text:
            attachments.jokes.append(",".join(buffer_photos))
        else:
            attachments.photos += buffer_photos

    return attachments


def handle_hent_group_posts(
    posts: list[WallWallpostFull], border_time: int = 0
) -> VkAttachments:
    attachments = VkAttachments()

    posts_with_attachments = list(
        filter(lambda x: x.attachments and x.date and (x.date >= border_time), posts)
    )

    for post in posts_with_attachments:
        text = post.text.lower() if post.text else ""
        buffer_photo, _ = handle_post_attachments(post)

        if "joke" in text:
            attachments.horny_jokes += buffer_photo
        else:
            attachments.horny_photos += buffer_photo

    return attachments


async def update_databases(group_id: int):
    try:
        response, count, posts = await service_api.wall.get(owner_id=group_id, count=3)
        return posts[1]
    except:
        return None


if __name__ == "__main__":
    asyncio.run(get_wall_posts(group_id=-208044622))
