#    This file is part of the CompressorBot distribution.
#    Copyright (c) 2021 Danish_00
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
#    License can be found in < https://github.com/1Danish-00/CompressorBot/blob/main/License> .


from .funcn import *


async def screenshot(e):
    await e.edit("`Generating Screenshots...`")
    COUNT.append(e.chat_id)
    wah = e.pattern_match.group(1).decode("UTF-8")
    key = decode(wah)
    out, dl, thum, dtime = key.split(";")
    os.mkdir(wah)
    tsec = await genss(dl)
    fps = 10 / tsec
    ncmd = f"ffmpeg -i '{dl}' -vf fps={fps} -vframes 10 '{wah}/pic%01d.png'"
    process = await asyncio.create_subprocess_shell(
        ncmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    await process.communicate()
    try:
        pic = glob.glob(f"{wah}/*")
        await e.client.send_file(e.chat_id, pic)
        await e.client.send_message(
            e.chat_id,
            "Check Screenshots Above 😁",
            buttons=[
                [
                    Button.inline("GENERATE SAMPLE", data=f"gsmpl{wah}"),
                    Button.inline("COMPRESS", data=f"sencc{wah}"),
                ],
                [Button.inline("SKIP", data=f"skip{wah}")],
            ],
        )
        COUNT.remove(e.chat_id)
        shutil.rmtree(wah)
    except Exception:
        COUNT.remove(e.chat_id)
        shutil.rmtree(wah)
        return


async def stats(e):
    try:
        wah = e.pattern_match.group(1).decode("UTF-8")
        wh = decode(wah)
        out, dl, thum, dtime = wh.split(";")
        ot = hbs(int(Path(out).stat().st_size))
        ov = hbs(int(Path(dl).stat().st_size))
        ans = f"Downloaded:\n{ov}\n\nCompressing:\n{ot}"
        await e.answer(ans, cache_time=0, alert=True)
    except BaseException:
        await e.answer("Someting Went Wrong 🤔\nResend Media", cache_time=0, alert=True)


async def encc(e):
    try:
        es = dt.now()
        COUNT.append(e.chat_id)
        wah = e.pattern_match.group(1).decode("UTF-8")
        wh = decode(wah)
        out, dl, thum, dtime = wh.split(";")
        nn = await e.edit(
            "`Compressing..`",
            buttons=[
                [Button.inline("STATS", data=f"stats{wah}")],
                [Button.inline("CANCEL PROCESS", data=f"skip{wah}")],
            ],
        )
        cmd = f"ffmpeg -i '{dl}' -preset superfast -vf scale=1024:-1 -vcodec libx265 -crf 24 -c:a aac -b:a 96k '{out}' -y"
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        er = stderr.decode()
        print(f'[stdout]\n{stdout.decode()}')
        try:
            if er:
                await e.edit(str(er) + "\n\n**ERROR** Contact @danish_00")
                COUNT.remove(e.chat_id)
                os.remove(dl)
                return os.remove(out)
        except BaseException:
            pass
        ees = dt.now()
        ttt = time.time()
        await nn.delete()
        nnn = await e.client.send_message(e.chat_id, "`Uploading...`")
        ds = await e.client.send_file(
            e.chat_id,
            file=f"{out}",
            force_document=True,
            thumb=thum,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, nnn, ttt, "uploading..", file=f"{out}")
            ),
        )
        org = int(Path(dl).stat().st_size)
        com = int(Path(out).stat().st_size)
        pe = 100 - ((com / org) * 100)
        per = str(f"{pe:.2f}") + "%"
        eees = dt.now()
        x = dtime
        xx = ts(int((ees - es).seconds) * 1000)
        xxx = ts(int((eees - ees).seconds) * 1000)
        a1 = await info(dl, e)
        a2 = await info(out, e)
        dk = await ds.reply(
            f"Original Size : {hbs(org)}\nCompressed Size : {hbs(com)}\nCompressed Percentage : {per}\n\nMediainfo: [Before]({a1})//[After]({a2})\n\nDownloaded in {x}\nCompressed in {xx}\nUploaded in {xxx}",
            link_preview=False,
        )
        await ds.forward_to(LOG)
        await dk.forward_to(LOG)
        await nnn.delete()
        COUNT.remove(e.chat_id)
        os.remove(dl)
        os.remove(out)
    except BaseException:
        return COUNT.remove(e.chat_id)


async def sample(e):
    wah = e.pattern_match.group(1).decode("UTF-8")
    wh = decode(wah)
    COUNT.append(e.chat_id)
    out, dl, thum, dtime = wh.split(";")
    ss, dd = await duration_s(dl)
    xxx = await e.edit(
        "`Generating Sample...`",
        buttons=[
            [Button.inline("STATS", data=f"stats{wah}")],
            [Button.inline("CANCEL PROCESS", data=f"skip{wah}")],
        ],
    )
    ncmd = f"ffmpeg -i '{dl}' -preset superfast -ss {ss} -to {dd} -vf scale=1024:-1 -c:v libx265 -crf 24 -c:a aac -b:a 96k '{out}'"
    process = await asyncio.create_subprocess_shell(
        ncmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    er = stderr.decode()
    print(f'[stdout]\n{stdout.decode()}')
    try:
        if er:
            await e.edit(str(er) + "\n\n**ERROR** Contact @danish_00")
            COUNT.remove(e.chat_id)
            os.remove(dl)
            os.remove(out)
            return
    except BaseException:
        pass
    stdout.decode()
    ttt = time.time()
    try:
        ds = await e.client.send_file(
            e.chat_id,
            file=f"{out}",
            force_document=False,
            thumb=thum,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, xxx, ttt, "uploading..", file=f"{out}")
            ),
            buttons=[
                [
                    Button.inline("SCREENSHOTS", data=f"sshot{wah}"),
                    Button.inline("COMPRESS", data=f"sencc{wah}"),
                ],
                [Button.inline("SKIP", data=f"skip{wah}")],
            ],
        )
        COUNT.remove(e.chat_id)
        os.remove(out)
        await xxx.delete()
    except BaseException:
        COUNT.remove(e.chat_id)
        os.remove(out)
        return


async def encod(event):
    try:
        if not event.is_private:
            return
        user = await event.get_chat()
        if not event.media:
            return
        try:
            if "video" not in event.media.document.mime_type.split("/"):
                return
        except BaseException:
            return
        try:
            oc = event.fwd_from.from_id.user_id
            occ = (await event.client.get_me()).id
            if oc == occ:
                return await event.reply("`This Video File is already Compressed 😑😑.`")
        except BaseException:
            pass
        xxx = await event.reply("`Downloading...`")
        pp = []
        # async for x in event.client.iter_participants("ensemblygroup"):
        #    pp.append(x.id)
        # if (user.id) not in pp:
        #    return await xxx.edit(
        #        "U Must Subscribe This Channel To Use This Bot",
        #       buttons=[Button.url("JOIN CHANNEL", url="t.me/ensemblygroup")],
        #   )
        if len(COUNT) > 4 and user.id != OWNER:
            llink = (await event.client(cl(LOG))).link
            return await xxx.edit(
                "Overload Already 5 Process Running",
                buttons=[Button.url("Working Status", url=llink)],
            )
        if user.id in COUNT and user.id != OWNER:
            return await xxx.edit(
                "Already Your 1 Request Processing\nKindly Wait For it to Finish"
            )
        COUNT.append(user.id)
        s = dt.now()
        ttt = time.time()
        await event.forward_to(LOG)
        gg = await event.client.get_entity(user.id)
        name = f"[{get_display_name(gg)}](tg://user?id={user.id})"
        await event.client.send_message(
            LOG, f"{len(COUNT)} Downloading Started for user - {name}"
        )
        dir = f"downloads/{user.id}/"
        if not os.path.isdir(dir):
            os.mkdir(dir)
        try:
            dl = await event.client.download_media(
                event.media,
                dir,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, xxx, ttt, "Downloading")
                ),
            )
        except BaseException:
            COUNT.remove(user.id)
            return os.remove(dl)
        es = dt.now()
        kk = dl.split("/")[-1]
        aa = kk.split(".")[-1]
        rr = f"encode/{user.id}"
        if not os.path.isdir(rr):
            os.mkdir(rr)
        bb = kk.replace(f".{aa}", " compressed.mkv")
        if '1080p' in bb:
            cc = bb.replace("1080p", "576p")
        elif '720p' in bb:
            cc = bb.replace("720p", "576p")
        else:
            cc = bb
        out = f"{rr}/{cc}"
        thum = "75ee20ec8d8c8bba84f02.jpg"
        dtime = ts(int((es - s).seconds) * 1000)
        hehe = f"{out};{dl};{thum};{dtime}"
        key = code(hehe)
        await xxx.delete()
        inf = await info(dl, event)
        COUNT.remove(user.id)
        await event.client.send_message(
            event.chat_id,
            f"🐠DOWNLODING COMPLETED!!🐠",
            buttons=[
                [
                    Button.inline("GENERATE SAMPLE", data=f"gsmpl{key}"),
                    Button.inline("SCREENSHOTS", data=f"sshot{key}"),
                ],
                [Button.url("MEDIAINFO", url=inf)],
                [Button.inline("COMPRESS", data=f"sencc{key}")],
            ],
        )
    except BaseException:
        return COUNT.remove(user.id)


async def customenc(e, key):
    es = dt.now()
    COUNT.append(e.chat_id)
    wah = key
    wh = decode(wah)
    out, dl, thum, dtime = wh.split(";")
    nn = await e.edit(
        "`Compressing..`",
        buttons=[
            [Button.inline("STATS", data=f"stats{wah}")],
            [Button.inline("CANCEL PROCESS", data=f"skip{wah}")],
        ],
    )
    cmd = f"ffmpeg -i '{dl}' -preset superfast -vf scale=1024:-1 -vcodec libx265 -crf 24 -c:a aac -b:a 96k '{out}' -y"
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    er = stderr.decode()
    print(f'[stdout]\n{stdout.decode()}')
    try:
        if er:
            await e.edit(str(er) + "\n\n**ERROR** Contact @danish_00")
            COUNT.remove(e.chat_id)
            os.remove(dl)
            return os.remove(out)
    except BaseException:
        pass
    stdout.decode()
    ees = dt.now()
    ttt = time.time()
    await nn.delete()
    nnn = await e.client.send_message(e.chat_id, "`Uploading...`")
    try:
        ds = await e.client.send_file(
            e.chat_id,
            file=f"{out}",
            force_document=True,
            thumb=thum,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, nnn, ttt, "uploading..", file=f"{out}")
            ),
        )
    except BaseException:
        COUNT.remove(e.chat_id)
        os.remove(dl)
        return os.remove(out)
    org = int(Path(dl).stat().st_size)
    com = int(Path(out).stat().st_size)
    pe = 100 - ((com / org) * 100)
    per = str(f"{pe:.2f}") + "%"
    eees = dt.now()
    x = dtime
    xx = ts(int((ees - es).seconds) * 1000)
    xxx = ts(int((eees - ees).seconds) * 1000)
    a1 = await info(dl, e)
    a2 = await info(out, e)
    dk = await ds.reply(
        f"Original Size : {hbs(org)}\nCompressed Size : {hbs(com)}\nCompressed Percentage : {per}\n\nMediainfo: [Before]({a1})//[After]({a2})\n\nDownloaded in {x}\nCompressed in {xx}\nUploaded in {xxx}",
        link_preview=False,
    )
    await ds.forward_to(LOG)
    await dk.forward_to(LOG)
    await nnn.delete()
    COUNT.remove(e.chat_id)
    os.remove(dl)
    os.remove(out)
