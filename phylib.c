#include "phylib.h"

phylib_object *phylib_new_still_ball (unsigned char number, phylib_coord *pos){

    //Allocating Memory
    phylib_object * new_still = (phylib_object *)malloc(sizeof(phylib_object));

    if(new_still == NULL){
        return NULL;
    }

    //Setting type to be a still ball
    new_still->type = PHYLIB_STILL_BALL;

    //Assigning the attributes
    new_still->obj.still_ball.number = number;
    new_still->obj.still_ball.pos = *pos;

    return new_still;

}

phylib_object *phylib_new_rolling_ball (unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc){

    //Allocate memory
    phylib_object * new_rolling = (phylib_object *)malloc(sizeof(phylib_object));

    if(new_rolling == NULL){
        return NULL;
    }

    //Assign Attributes
    new_rolling->type = PHYLIB_ROLLING_BALL;

    new_rolling->obj.rolling_ball.number = number;
    new_rolling->obj.rolling_ball.pos = *pos;
    new_rolling->obj.rolling_ball.vel = *vel;
    new_rolling->obj.rolling_ball.acc = *acc;

    return new_rolling;

}

phylib_object *phylib_new_hole (phylib_coord *pos){


    //Allocating memory
    phylib_object * new_hole = (phylib_object *)malloc(sizeof(phylib_object));

    if(new_hole == NULL){
        return NULL;
    }

    //Assigning the attributes
    new_hole->type = PHYLIB_HOLE;
    new_hole->obj.hole.pos = *pos;

    return new_hole;
}

phylib_object *phylib_new_hcushion (double y){

    //Allocating memory
    phylib_object * new_hcushion = (phylib_object *)malloc(sizeof(phylib_object));

    if(new_hcushion == NULL){
        return NULL;
    }

    //Assigning the attributes
    new_hcushion->type = PHYLIB_HCUSHION;
    new_hcushion->obj.hcushion.y = y;

    return new_hcushion;
}

phylib_object *phylib_new_vcushion (double x){

    //Allocating memory
    phylib_object * new_vcushion = (phylib_object *)malloc(sizeof(phylib_object));

    if(new_vcushion == NULL){
        return NULL;
    }

    //Assigning the attributes
    new_vcushion->type = PHYLIB_VCUSHION;
    new_vcushion->obj.vcushion.x = x;

    return new_vcushion;
}

phylib_table *phylib_new_table (void){
    //Assigning the attributes
    phylib_table * new_table = (phylib_table *)malloc(sizeof(phylib_table));

    if(new_table == NULL){
        return NULL;
    }

    new_table->time = 0.0;

    //Set all pointers in table to NULL
    for(int i=0; i<PHYLIB_MAX_OBJECTS; i++){
        new_table->object[i] = NULL;
    }

    //Add all the cushions and new holes at appropritate locations
    new_table->object[0] = phylib_new_hcushion(0.0);
    new_table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    new_table->object[2] = phylib_new_vcushion(0.0);
    new_table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    new_table->object[4] = phylib_new_hole(&(phylib_coord){0.0, 0.0});
    new_table->object[5] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_WIDTH});
    new_table->object[6] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH});
    new_table->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0.0});
    new_table->object[8] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH});
    new_table->object[9] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH});


    return new_table;
}

void phylib_copy_object (phylib_object **dest, phylib_object **src){

    //Checj if src is NULL
    if(*src == NULL){
        *dest = NULL;
        return;
    }

    //Allocate memory
    *dest = (phylib_object *)malloc(sizeof(phylib_object));

    if(*dest == NULL){
        return;
    }

    //Copy the data from src to dest using memcpy
    memcpy(*dest, *src, sizeof(phylib_object));

}

phylib_table *phylib_copy_table (phylib_table *table){

    //Allocate the space for new table
    phylib_table *new_table = (phylib_table *)malloc(sizeof(phylib_table));

    if (new_table == NULL) {
        return NULL;
    }
    //Copy the contents from old table
    memcpy(new_table, table, sizeof(phylib_table));

    //Also copy data that the pointers are pointing to using phylib copy object and also set the null pointers
    for (int i=0; i <PHYLIB_MAX_OBJECTS; ++i) {
        new_table->object[i] = NULL;
        if (table->object[i] != NULL) {
            phylib_copy_object(&(new_table->object[i]), &(table->object[i]));
        }
    }

    return new_table;
}

void phylib_add_object (phylib_table *table, phylib_object *object){

    //Check for null
    if(object == NULL || table == NULL){
        return;
    }

    //Check to find the first null location and set the pointer equal to the object
    for(int i=0; i<PHYLIB_MAX_OBJECTS; i++){
        if(table->object[i] == NULL){
            table->object[i] = object;
            return;
        }
    }
}

void phylib_free_table (phylib_table *table){
    if(table == NULL){
        return;
    }

    //First free the pointer array using a loop, and set them to null
    for(int i=0; i<PHYLIB_MAX_OBJECTS; i++){
        free(table->object[i]);   
        table->object[i] = NULL; 
    }
    //Now free the table
    free(table);
}

phylib_coord phylib_sub (phylib_coord c1, phylib_coord c2){

    phylib_coord result;

    //Doing the formula c1 - c2 and also subtracting x and y components
    result.x = (c1.x) - (c2.x);
    result.y = (c1.y) - (c2.y);

    return result;
}

double phylib_length (phylib_coord c){

    //Find x^2 and y^2 and adding them
    double x2 = (c.x) * (c.x);
    double y2 = (c.y) * (c.y);
    double len = x2 + y2;

    //Take the square root of addition
    double result = sqrt(len);  

    return result;
}

double phylib_dot_product (phylib_coord a, phylib_coord b){

    //Multiply the x components and y components and add them
    double result = (a.x * b.x) + (a.y * b.y);

    return result;
}

double phylib_distance (phylib_object *obj1, phylib_object *obj2){
    //Error Checking
    if(obj1->type != PHYLIB_ROLLING_BALL){
        return -1.0;
    }


    if(obj2->type == PHYLIB_ROLLING_BALL ){
        //Subtract the positions from both the objects
        phylib_coord delta = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos); 

        //Find distance using length and subtract the ball diameter
        double distance = phylib_length(delta) - PHYLIB_BALL_DIAMETER;

        return distance;


    } else if (obj2->type == PHYLIB_STILL_BALL){

        //Same thing as above but now for the still ball
        phylib_coord delta = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos); 

        double distance = phylib_length(delta) - PHYLIB_BALL_DIAMETER;

        return distance;

        
    } else if (obj2->type ==  PHYLIB_HOLE){

        //Same subtraction for finding the position
        phylib_coord delta = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos); 

        //But now subtract the Hole radius
        double distance = phylib_length(delta) - PHYLIB_HOLE_RADIUS;

        return distance;

    } else if (obj2->type == PHYLIB_VCUSHION) {

        double x2 = obj2->obj.vcushion.x;

        //Find the position by subtracting only the x components and subtract radius

        double distance = fabs(obj1->obj.rolling_ball.pos.x - x2) - PHYLIB_BALL_RADIUS;

        return distance;
        
    } else if (obj2->type == PHYLIB_HCUSHION){

        double y2 = obj2->obj.hcushion.y;

        //Same thing as X cushion but use the y component

        double distance = fabs(obj1->obj.rolling_ball.pos.y - y2) - PHYLIB_BALL_RADIUS;

        return distance;

    }
    
    return -1.0;   
}


void phylib_roll (phylib_object *new, phylib_object *old, double time){

    //Error checking
    if(new == NULL || old == NULL){
        return;
    }

    if(old->type != PHYLIB_ROLLING_BALL ){
        return;
    }

    if(new->type != PHYLIB_ROLLING_BALL){
        return;
    }

    //Doing the roll formula that is provided for both the x and y components
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + (old->obj.rolling_ball.vel.x * time) + ((0.5) * old->obj.rolling_ball.acc.x * (time * time));
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + (old->obj.rolling_ball.vel.y * time) + ((0.5) * old->obj.rolling_ball.acc.y * (time * time));

    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + (old->obj.rolling_ball.acc.x * time);
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + (old->obj.rolling_ball.acc.y * time);

    //Checking if the velocity has flipped by multiplying and seeinf if the result for both x and y components and set the acceleration and velocities to 0
    if ((new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x) < 0.0) {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }
    if ((new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y) < 0.0) {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }

}

unsigned char phylib_stopped (phylib_object *object){

    //Finding the velocity using phylib_length and check if the value is less than vel epsilon
    if(object->type != PHYLIB_ROLLING_BALL){
        return 0;
    }

    if (phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON) {
        // Convert the rolling ball to a still ball
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        object->obj.still_ball.pos.x = object->obj.rolling_ball.pos.x;
        object->obj.still_ball.pos.y = object->obj.rolling_ball.pos.y;

        // Return 1 to indicate that the ball was converted
        return 1;
    } 

    return 0;
}

void phylib_bounce (phylib_object **a, phylib_object **b){

    if((*a) == NULL || (*a)->type != PHYLIB_ROLLING_BALL){
        return;
    }

    switch ((*b)->type) {
        case PHYLIB_HCUSHION:

            //If we hit a h-cushion, make the y components of velocity and accleration negative 
            (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y * -1;
            (*a)->obj.rolling_ball.acc.y = (*a)->obj.rolling_ball.acc.y * -1;
            break;

        case PHYLIB_VCUSHION:

            //If we hit a v-cushion, make the x components of velocity and accleration negative 
            (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x * -1;
            (*a)->obj.rolling_ball.acc.x = (*a)->obj.rolling_ball.acc.x * -1;
            break;

        case PHYLIB_HOLE:
            //Free the ball cause we hit a hole
            free(*a);
            *a = NULL;
            break;
        
        case PHYLIB_STILL_BALL:

            //Make the still ball to rolling ball, move the still ball pos to rolling ball pos and set velocities and accelrations to 0
            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.pos.x = (*b)->obj.still_ball.pos.x;
            (*b)->obj.rolling_ball.pos.y = (*b)->obj.still_ball.pos.y;
            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.vel.y = 0.0;
            (*b)->obj.rolling_ball.acc.x = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;

            //No break statements


        case PHYLIB_ROLLING_BALL:{

            //Find the Relative position and velocity

            phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);

            phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

            //Dividing the x and y components by len of r_ab 
            double r_ab_len = phylib_length(r_ab);

            double n_x = r_ab.x / r_ab_len;
            double n_y = r_ab.y / r_ab_len;

            //Assign the values to the normal vector
            phylib_coord n = {n_x, n_y};

            //Find the dot product of normal vector and relative velocity
            double v_rel_n = phylib_dot_product(v_rel, n);

            //Updating the x and y velocites of a and b by subtracting from a and adding to b

            (*a)->obj.rolling_ball.vel.x -= (v_rel_n * n.x);
            (*a)->obj.rolling_ball.vel.y -= (v_rel_n * n.y);

            (*b)->obj.rolling_ball.vel.x += (v_rel_n * n.x);
            (*b)->obj.rolling_ball.vel.y += (v_rel_n * n.y);

            double speed_a = phylib_length((*a)->obj.rolling_ball.vel);
            double speed_b = phylib_length((*b)->obj.rolling_ball.vel);

            //Finding the spped of a and b using length

            // if speed of a and b is greater than vel epsilon than apply the formula

            if (speed_a > PHYLIB_VEL_EPSILON) {
                (*a)->obj.rolling_ball.acc.x = (-1 * (*a)->obj.rolling_ball.vel.x) / speed_a * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = (-1 * (*a)->obj.rolling_ball.vel.y) / speed_a * PHYLIB_DRAG;
            }

            if (speed_b > PHYLIB_VEL_EPSILON) {
                (*b)->obj.rolling_ball.acc.x = (-1 *(*b)->obj.rolling_ball.vel.x) / speed_b * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = (-1 *(*b)->obj.rolling_ball.vel.y) / speed_b * PHYLIB_DRAG;
            }

           break;
        }

        default:

          break;

    }


}

unsigned char phylib_rolling (phylib_table *t){

    if(t == NULL){
        return 0;
    }

    unsigned char count = 0;

    //Check to see if the object is not null and it is a rolling ball
    for(int i=0; i<PHYLIB_MAX_OBJECTS; i++){
        if(t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL){
            count++;
        }
    }

    return count;

}

phylib_table *phylib_segment(phylib_table *table) {
    
    //Check if 0 balls are rolling
    if(phylib_rolling(table) == 0){
        return NULL;
    }

    //Make a copy of the table
    phylib_table *copy = phylib_copy_table(table);

    //Start the time at sim rate

    double time = PHYLIB_SIM_RATE;

    while(time < PHYLIB_MAX_TIME){

        //First roll all the object in this loop and keeping the same time
        for(int i=0; i<PHYLIB_MAX_OBJECTS; i++){
            if(copy->object[i] && copy->object[i]->type == PHYLIB_ROLLING_BALL){
                phylib_roll(copy->object[i], table->object[i] ,time);
            }     
        }

        //Now check if the distance between a rolling ball and any other object is less than 0 then apply the bounce to both object
        for(int i=0; i<PHYLIB_MAX_OBJECTS; i++){
            for(int j=0; j<PHYLIB_MAX_OBJECTS; j++){
                if(i!= j && copy->object[i] && copy->object[i]->type == PHYLIB_ROLLING_BALL && copy->object[j] && (phylib_distance(copy->object[i], copy->object[j]) < 0.0 )){
                    phylib_bounce(&copy->object[i], &copy->object[j]);
                    copy->time += time;
                    return copy;
                    }
                }
                //Check to see if a rolling ball has stopped then return the table
                if(copy->object[i] && copy->object[i]->type == PHYLIB_ROLLING_BALL && phylib_stopped(copy->object[i])){
                    copy->time += time;
                    return copy;
                }
            
        }
        time+= PHYLIB_SIM_RATE;
    }

    copy->time += time;
    return copy;
}

char *phylib_object_string( phylib_object *object ) {
    static char string[80];

    if (object==NULL) {
        snprintf( string, 80, "NULL;" );
        return string;
    }

    switch (object->type) {

        case PHYLIB_STILL_BALL:

            snprintf( string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x,
            object->obj.still_ball.pos.y );
            break;

        case PHYLIB_ROLLING_BALL:

            snprintf( string, 80,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object->obj.rolling_ball.number,
            object->obj.rolling_ball.pos.x,
            object->obj.rolling_ball.pos.y,
            object->obj.rolling_ball.vel.x,
            object->obj.rolling_ball.vel.y,
            object->obj.rolling_ball.acc.x,
            object->obj.rolling_ball.acc.y );
            break;

        case PHYLIB_HOLE:
            snprintf( string, 80,
            "HOLE (%6.1lf,%6.1lf)",
            object->obj.hole.pos.x,
            object->obj.hole.pos.y );
            break;

        case PHYLIB_HCUSHION:

            snprintf( string, 80,
            "HCUSHION (%6.1lf)",
            object->obj.hcushion.y );
            break;

        case PHYLIB_VCUSHION:

            snprintf( string, 80,
            "VCUSHION (%6.1lf)",
            object->obj.vcushion.x );
            break;

    }
    
    return string;
}
