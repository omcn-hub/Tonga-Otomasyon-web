<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash; 

class Admins extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    { 
        $items = [[
            'name' => 'admin',
            'tc' => '11111111111',
            'title' => 'Admin',
            'phone' => '1111111111',
            'email' => 'admin@admin.com',
            'password' => Hash::make('123456'), 
            'is_active' => 1, 
        ]];  

        DB::table('admin')->insert($items);
    }
}
