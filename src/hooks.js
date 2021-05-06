import dotenv from 'dotenv'
dotenv.config()

import mongoUtil from '$lib/db'
mongoUtil.init()
