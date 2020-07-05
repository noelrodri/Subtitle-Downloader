def is_video_file(filename):
    video_extns = [
        '.avi',
        '.divx',
        '.mkv',
        '.mp4',
        '.ogg',
        '.rm',
        '.rmvb',
        '.vob',
        '.x264',
        '.xvid',
        '.wmv',
        '.mov',
        '.mpeg',
    ]
    if os.path.splitext(filename)[1].lower() in video_extns:
        return True


def calc_file_hash(filepath):

    try:
        longlongformat = 'q'  # long long
        bytesize = struct.calcsize(longlongformat)

        f = open(filepath, 'rb')

        filesize = os.path.getsize(filepath)
        filehash = filesize

        if filesize < 65536 * 2:
            raise Exception('SizeError: Minimum file size must be 120Kb'
                            )

        for x in range(65536 // bytesize):
            buffer = f.read(bytesize)
            (l_value, ) = struct.unpack(longlongformat, buffer)
            filehash += l_value
            filehash = filehash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

        f.seek(max(0, filesize - 65536), 0)
        for x in range(65536 // bytesize):
            buffer = f.read(bytesize)
            (l_value, ) = struct.unpack(longlongformat, buffer)
            filehash += l_value
            filehash = filehash & 0xFFFFFFFFFFFFFFFF

        f.close()
        filehash = '%016x' % filehash
        return filehash
    except IOError:
        raise


def unicode(arg):
    return str(arg)


def clean_name(name):
    name = re.sub('[\W_]+', ' ', unicode(name.lower()))
    name = re.sub(r"\s+", ' ', name)
    return name


def download_url_content(url, referer=None, timeout=10):
    ''' Downloads and returns the contents of the given url.'''

    if referer:
        request_headers['Referer'] = referer
    else:
        request_headers['Referer'] = url

    try:
        x = requests.get(url, headers=request_headers, timeout=timeout)
    except Exception as e:
        print(e)
        raise e

    if x.status_code != 200:
        raise Exception("Invalid Response From Server")

    return x.content


def guess_file_data(filename):
    filename = clean_name(filename)
    matches_tvshow = tv_show_regex.match(filename)
    matches_movie = movie_regex.match(filename)

    if matches_tvshow and not matches_movie:
        (tvshow, season, episode, teams) = matches_tvshow.groups()
        teams = teams.split()
        data = {
            'type': 'tvshow',
            'name': tvshow.strip(),
            'season': int(season),
            'episode': int(episode),
            'teams': teams,
        }
    elif matches_movie:
        (movie, year, teams) = matches_movie.groups()
        teams = teams.split()
        part = None
        if 'cd1' in teams:
            teams.remove('cd1')
            part = 1
        if 'cd2' in teams:
            teams.remove('cd2')
            part = 2
        data = {
            'type': 'movie',
            'name': movie.strip(),
            'year': year,
            'teams': teams,
            'part': part,
        }
    else:
        data = {'type': 'unknown', 'name': filename, 'teams': []}

    return data


def check_tvshow(filename):
    fname = unicode(filename.lower())
    guessed_file_data = guess_file_data(fname)
    return guessed_file_data['type'] == 'tvshow'


def catch_all(site, files):
    try:
        print(site)
    except Exception as e:
        print(e)


def save_subs(content, full_path, other_details=None):
    open(full_path, 'wb').write(content)


def process_queue(queue):
    addic7ed_list = []
    opensubs_dict = {}

    for video in queue:
        if video['type'] == 'Addic7ed':
            addic7ed_list.append(video)

    if addic7ed_list:
        ad = Addic7ed()
        ad.process(addic7ed_list)


def path():
    print(os.path)
