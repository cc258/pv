import React, {useState, useEffect} from 'react'
import {useAtom} from 'jotai';

import { getCategories } from './categories.jotai.js';

const Categories = () => {
    const [categories, setCategories] = useAtom(getCategories);

    useEffect(() => {
        setCategories()
    }, [])


    return (

        <div className="flex flex-wrap w-full p-6 gap-2 md:gap-2 items-center text-sm text-white md:text-md">
            {
                categories.map((i,k)=>{
                    return <a key={k} href={`/category?category_id=${i.id}&category_name=${i.name}`} className="bg-cyan-500 rounded px-2 py-1">
                        {i.name}
                    </a>
                })
            }
        </div>
    );
};

export default Categories;
