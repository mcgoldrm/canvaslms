def get_user_courses():
    token = os.getenv('CANVAS_API_TOKEN')
    if not token:
        print("Error: CANVAS_API_TOKEN is not set.")
        return []

    base_url = 'https://mcpsmd.instructure.com'
    endpoint = f'{base_url}/api/v1/users/self/courses?enrollment_type=teacher'
    headers = {'Authorization': f'Bearer {token}'}

    all_courses = []

    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        all_courses.extend(response.json())

        while 'next' in response.links:
            next_url = response.links['next']['url']
            response = requests.get(next_url, headers=headers)

            # Add the courses from the current page to the list
            all_courses.extend(response.json())

            all_courses = sorted(all_courses, key=lambda x: x['name'])
            print(all_courses)
            return all_courses

    else:
        print(f"Failed to fetch courses: {response.status_code}")
        print(response.text)
        return []
